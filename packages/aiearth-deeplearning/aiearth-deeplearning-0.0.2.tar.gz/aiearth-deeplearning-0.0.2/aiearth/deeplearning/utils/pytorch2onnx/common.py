# -*- conding: utf-8 -*-
# Copyright (c) OpenMMLab. All rights reserved.
import argparse
from copy import copy
import os
from functools import partial

import numpy as np
import onnxruntime as rt
import torch
import torch._C
import torch.serialization
from torch import nn

import mmcv
from mmcv import DictAction
from mmcv.onnx import register_extra_symbolics
from mmcv.runner import load_checkpoint

from aiearth.deeplearning.engine.mmseg.apis import show_result_pyplot
from aiearth.deeplearning.engine.mmseg.apis.inference import LoadImage
from aiearth.deeplearning.engine.mmseg.datasets.pipelines import Compose
from aiearth.deeplearning.engine.mmseg.models import build_segmentor
from aiearth.deeplearning.engine.mmseg.ops import resize

torch.manual_seed(3)


def _convert_batchnorm(module):
    module_output = module
    if isinstance(module, torch.nn.SyncBatchNorm):
        module_output = torch.nn.BatchNorm2d(
            module.num_features,
            module.eps,
            module.momentum,
            module.affine,
            module.track_running_stats,
        )
        if module.affine:
            module_output.weight.data = module.weight.data.clone().detach()
            module_output.bias.data = module.bias.data.clone().detach()
            # keep requires_grad unchanged
            module_output.weight.requires_grad = module.weight.requires_grad
            module_output.bias.requires_grad = module.bias.requires_grad
        module_output.running_mean = module.running_mean
        module_output.running_var = module.running_var
        module_output.num_batches_tracked = module.num_batches_tracked
    for name, child in module.named_children():
        module_output.add_module(name, _convert_batchnorm(child))
    del module
    return module_output


def _demo_mm_inputs(input_shape, num_classes):
    """Create a superset of inputs needed to run test or train batches.

    Args:
        input_shape (tuple):
            input batch dimensions
        num_classes (int):
            number of semantic classes
    """
    (N, C, H, W) = input_shape
    rng = np.random.RandomState(0)
    imgs = rng.rand(*input_shape)
    if num_classes == 1:
        num_classes = 2
    segs = rng.randint(low=0, high=num_classes - 1,
                       size=(N, 1, H, W)).astype(np.uint8)
    img_metas = [
        {
            "img_shape": (H, W, C),
            "ori_shape": (H, W, C),
            "pad_shape": (H, W, C),
            "filename": "<demo>.png",
            "scale_factor": 1.0,
            "flip": False,
        }
        for _ in range(N)
    ]
    mm_inputs = {
        "imgs": torch.FloatTensor(imgs).requires_grad_(True),
        "img_metas": img_metas,
        "gt_semantic_seg": torch.LongTensor(segs),
    }
    return mm_inputs


def _prepare_input_img(img_path, test_pipeline, shape=None, rescale_shape=None):
    # build the data pipeline
    if shape is not None:
        test_pipeline[1]["img_scale"] = (shape[1], shape[0])
    test_pipeline[1]["transforms"][0]["keep_ratio"] = False
    test_pipeline = [LoadImage()] + test_pipeline[1:]
    test_pipeline = Compose(test_pipeline)
    # prepare data
    data = dict(img=img_path)
    data = test_pipeline(data)
    imgs = data["img"]
    img_metas = [i.data for i in data["img_metas"]]

    if rescale_shape is not None:
        for img_meta in img_metas:
            img_meta["ori_shape"] = tuple(rescale_shape) + (3,)

    mm_inputs = {"imgs": imgs, "img_metas": img_metas}

    return mm_inputs


def _update_input_img(img_list, img_meta_list, update_ori_shape=False):
    # update img and its meta list
    N, C, H, W = img_list[0].shape
    img_meta = img_meta_list[0][0]
    img_shape = (H, W, C)
    if update_ori_shape:
        ori_shape = img_shape
    else:
        ori_shape = img_meta["ori_shape"]
    pad_shape = img_shape
    new_img_meta_list = [
        [
            {
                "img_shape": img_shape,
                "ori_shape": ori_shape,
                "pad_shape": pad_shape,
                "filename": img_meta["filename"],
                "scale_factor": (
                    img_shape[1] / ori_shape[1],
                    img_shape[0] / ori_shape[0],
                )
                * 2,
                "flip": False,
            }
            for _ in range(N)
        ]
    ]

    return img_list, new_img_meta_list


def pytorch2onnx(
    model,
    mm_inputs,
    opset_version=11,
    show=False,
    output_file="tmp.onnx",
    verify=False,
    dynamic_export=False,
):
    """Export Pytorch model to ONNX model and verify the outputs are same
    between Pytorch and ONNX.

    Args:
        model (nn.Module): Pytorch model we want to export.
        mm_inputs (dict): Contain the input tensors and img_metas information.
        opset_version (int): The onnx op version. Default: 11.
        show (bool): Whether print the computation graph. Default: False.
        output_file (string): The path to where we store the output ONNX model.
            Default: `tmp.onnx`.
        verify (bool): Whether compare the outputs between Pytorch and ONNX.
            Default: False.
        dynamic_export (bool): Whether to export ONNX with dynamic axis.
            Default: False.
    """
    model.cpu().eval()
    test_mode = model.test_cfg.mode

    if isinstance(model.decode_head, nn.ModuleList):
        num_classes = model.decode_head[-1].num_classes
    else:
        num_classes = model.decode_head.num_classes

    imgs = mm_inputs.pop("imgs")
    img_metas = mm_inputs.pop("img_metas")

    img_list = [img[None, :] for img in imgs]
    img_meta_list = [[img_meta] for img_meta in img_metas]
    # update img_meta
    img_list, img_meta_list = _update_input_img(img_list, img_meta_list)

    # replace original forward function
    origin_forward = model.forward
    # model.forward = partial(
    #    model.forward,
    #    img_metas=img_meta_list,
    #    return_loss=False,
    #    rescale=True)
    dynamic_axes = None
    if dynamic_export:
        if test_mode == "slide":
            dynamic_axes = {"input": {0: "batch"}, "output": {1: "batch"}}
        else:
            dynamic_axes = {
                "input": {0: "batch", 2: "height", 3: "width"},
                "output": {1: "batch", 2: "height", 3: "width"},
            }

    register_extra_symbolics(opset_version)
    with torch.no_grad():
        torch.onnx.export(
            model,
            (img_list, img_meta_list, False, dict(rescale=True)),
            output_file,
            input_names=["input"],
            output_names=["output"],
            export_params=True,
            keep_initializers_as_inputs=False,
            verbose=show,
            opset_version=opset_version,
            dynamic_axes=dynamic_axes,
        )
        print(f"Successfully exported ONNX model: {output_file}")
    os.system("python3 -m onnxsim {} {}".format(output_file, output_file))
    model.forward = origin_forward

    if verify:
        # check by onnx
        import onnx

        onnx_model = onnx.load(output_file)
        onnx.checker.check_model(onnx_model)

        if dynamic_export and test_mode == "whole":
            # scale image for dynamic shape test
            img_list = [resize(_, scale_factor=1.5) for _ in img_list]
            # concate flip image for batch test
            flip_img_list = [_.flip(-1) for _ in img_list]
            img_list = [
                torch.cat((ori_img, flip_img), 0)
                for ori_img, flip_img in zip(img_list, flip_img_list)
            ]

            # update img_meta
            img_list, img_meta_list = _update_input_img(
                img_list, img_meta_list, test_mode == "whole"
            )

        # check the numerical value
        # get pytorch output
        with torch.no_grad():
            pytorch_result = model(img_list, img_meta_list, return_loss=False)
            pytorch_result = np.stack(pytorch_result, 0)

        # get onnx output
        input_all = [node.name for node in onnx_model.graph.input]
        input_initializer = [
            node.name for node in onnx_model.graph.initializer]
        net_feed_input = list(set(input_all) - set(input_initializer))
        assert len(net_feed_input) == 1
        sess = rt.InferenceSession(output_file)
        onnx_result = sess.run(None, {net_feed_input[0]: img_list[0].detach().numpy()})[
            0
        ][0]
        # show segmentation results
        if show:
            import cv2
            import os.path as osp

            img = img_meta_list[0][0]["filename"]
            if not osp.exists(img):
                img = imgs[0][:3, ...].permute(1, 2, 0) * 255
                img = img.detach().numpy().astype(np.uint8)
                ori_shape = img.shape[:2]
            else:
                ori_shape = LoadImage()({"img": img})["ori_shape"]

            # resize onnx_result to ori_shape
            onnx_result_ = cv2.resize(
                onnx_result[0].astype(np.uint8), (ori_shape[1], ori_shape[0])
            )
            show_result_pyplot(
                model,
                img,
                (onnx_result_,),
                palette=model.PALETTE,
                block=False,
                title="ONNXRuntime",
                opacity=0.5,
            )

            # resize pytorch_result to ori_shape
            pytorch_result_ = cv2.resize(
                pytorch_result[0].astype(
                    np.uint8), (ori_shape[1], ori_shape[0])
            )
            show_result_pyplot(
                model,
                img,
                (pytorch_result_,),
                title="PyTorch",
                palette=model.PALETTE,
                opacity=0.5,
            )
        # compare results
        np.testing.assert_allclose(
            pytorch_result.astype(np.float32) / num_classes,
            onnx_result.astype(np.float32) / num_classes,
            rtol=1e-5,
            atol=1e-5,
            err_msg="The outputs are different between Pytorch and ONNX",
        )
        print("The outputs are same between Pytorch and ONNX")

def to_onnx(cfg, output_path, checkpoint_path=None, shape=(1024, 1024)):
    cfg = copy(cfg)
    cfg.model.pretrained = None

    assert len(shape) == 2
    input_shape = (
        1,
        3,
    ) + tuple(shape)

    test_mode = cfg.model.test_cfg.mode

    # build the model and load checkpoint
    cfg.model.train_cfg = None
    segmentor = build_segmentor(
        cfg.model, train_cfg=None, test_cfg=cfg.get("test_cfg"))
    # convert SyncBN to BN
    segmentor = _convert_batchnorm(segmentor)

    if checkpoint_path:
        checkpoint = load_checkpoint(
            segmentor, checkpoint_path, map_location="cpu")

    if isinstance(segmentor.decode_head, nn.ModuleList):
        num_classes = segmentor.decode_head[-1].num_classes
    else:
        num_classes = segmentor.decode_head.num_classes
    mm_inputs = _demo_mm_inputs(input_shape, num_classes)

    # convert model to onnx file
    pytorch2onnx(
        segmentor,
        mm_inputs,
        output_file=output_path,
    )
