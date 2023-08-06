import cv2, random, copy, mmcv, inspect
import numpy as np
from aiearth.deeplearning.engine.mmseg.datasets.builder import PIPELINES
from aiearth.deeplearning.engine.mmseg.datasets.pipelines.compose import Compose

try:
    import albumentations, ot, skimage
    from skimage import segmentation
except ImportError:
    albumentations = None
    ot = None
    skimage = None
    segmentation = None


@PIPELINES.register_module()
class RandomROT90(object):
    """Randomly rotate the image by 90 degrees.
    Args:
        degs (list[int]): A list of degrees to choose from.
    """
    def __init__(self, degs = [0, 90, 180, 270]):
        self.degs = degs
        
    def __call__(self, results):
        if 'rotate90' not in results:
            results['rotate90'] = True
        if results['rotate90']:
            if 'rotate_degree' not in results:
                results['rotate_degree'] = random.choice(self.degs)
        if results['rotate90']:
            results['img'] = np.rot90(results['img'], results['rotate_degree'] / 90)
            for key in results.get('seg_fields', []):
                results[key] = np.rot90(results[key], results['rotate_degree'] / 90).copy()
        return results
        
    def __repr__(self):
        repr_str = self.__class__.__name__
        return repr_str


@PIPELINES.register_module()
class Albu:
    """Albumentation augmentation.
    Adds custom transformations from Albumentations library.
    Please, visit `https://albumentations.readthedocs.io`
    to get more information.
    An example of ``transforms`` is as followed:
    .. code-block::
        [
            dict(
                type='ShiftScaleRotate',
                shift_limit=0.0625,
                scale_limit=0.0,
                rotate_limit=0,
                interpolation=1,
                p=0.5),
            dict(
                type='RandomBrightnessContrast',
                brightness_limit=[0.1, 0.3],
                contrast_limit=[0.1, 0.3],
                p=0.2),
            dict(type='ChannelShuffle', p=0.1),
            dict(
                type='OneOf',
                transforms=[
                    dict(type='Blur', blur_limit=3, p=1.0),
                    dict(type='MedianBlur', blur_limit=3, p=1.0)
                ],
                p=0.1),
        ]
    Args:
        transforms (list[dict]): A list of albu transformations
        bbox_params (dict): Bbox_params for albumentation `Compose`
        keymap (dict): Contains {'input key':'albumentation-style key'}
        skip_img_without_anno (bool): Whether to skip the image if no ann left
            after aug
    """

    def __init__(self,
                 transforms):
        self.transforms = copy.deepcopy(transforms)
        self.aug = albumentations.Compose([self.albu_builder(t) for t in self.transforms])

    def albu_builder(self, cfg):
        assert isinstance(cfg, dict) and 'type' in cfg
        args = cfg.copy()

        obj_type = args.pop('type')
        if mmcv.is_str(obj_type):
            if albumentations is None:
                raise RuntimeError('albumentations is not installed')
            obj_cls = getattr(albumentations, obj_type)
        elif inspect.isclass(obj_type):
            obj_cls = obj_type
        else:
            raise TypeError(
                f'type must be a str or valid type, but got {type(obj_type)}')

        if 'transforms' in args:
            args['transforms'] = [
                self.albu_builder(transform)
                for transform in args['transforms']
            ]

        return obj_cls(**args)

    def __call__(self, results):
        if 'gt_semantic_seg' in results:
            tmp = self.aug(image=results['img'], mask=results['gt_semantic_seg'])
            results['img'] = tmp['image']
            results['gt_semantic_seg'] = tmp['mask']
        else:
            tmp = self.aug(image=results['img'])
            results['img'] = tmp['image']
        return results

    def __repr__(self):
        repr_str = self.__class__.__name__ + f'(transforms={self.transforms})'
        return repr_str

@PIPELINES.register_module()
class CutMixSemi(object):
    """CutMix augmentation.
    Args:
        pre_transforms (list[dict]): A list of pre-transformations.
        p (float): The probability of applying CutMix.
        alpha (float): The hyperparameter of CutMix.
    
    add by gongyuan
    """
    def __init__(self, pre_transforms, p=1., alpha=1.0):
        self.pre_transforms=Compose(pre_transforms)
        self.p = p
        self.alpha = alpha

    def __call__(self, results, **kwargs):
        if random.random()<self.p:
            img_info=random.sample(results['img_infos'], 1)[0]
            tmp = self.pre_transforms(self.pre_pipeline(self.get_inputs(img_info), results))

            image1 = results['img']
            mask1 = results['gt_semantic_seg']
            image2 = tmp['img']
            mask2 = tmp['gt_semantic_seg']

            lam = np.random.beta(self.alpha, self.alpha)
            (bby1, bby2, bbx1, bbx2) = self.rand_bbox(image1.shape, lam)
            image1[bby1:bby2, bbx1:bbx2, :] = image2[bby1:bby2, bbx1:bbx2, :]
            mask1[bby1:bby2, bbx1:bbx2] = mask2[bby1:bby2, bbx1:bbx2]
            results['img'] = image1
            results['gt_semantic_seg'] = mask1
            results['cutmix'] = img_info
        else:
            results['cutmix'] = None
        return results

    def get_inputs(self, img_info):
        ann_info = img_info['ann']
        return dict(img_info=img_info, ann_info=ann_info)

    def pre_pipeline(self, results, original):
        """Prepare results dict for pipeline."""
        results['seg_fields'] = []
        results['img_prefix'] = original['img_prefix']
        results['seg_prefix'] = original['seg_prefix']
        return results

    def rand_bbox(self, img_shape, lam, margin=0., count=None):
        """Standard CutMix bounding-box that generates a random square bbox
        based on lambda value. This implementation includes support for
        enforcing a border margin as percent of bbox dimensions.
        Args:
            img_shape (tuple): Image shape as tuple
            lam (float): Cutmix lambda value
            margin (float): Percentage of bbox dimension to enforce as margin
                (reduce amount of box outside image). Default to 0.
            count (int, optional): Number of bbox to generate. Default to None
        """
        ratio = np.sqrt(1 - lam)
        img_h, img_w = img_shape[:2]
        cut_h, cut_w = int(img_h * ratio), int(img_w * ratio)
        margin_y, margin_x = int(margin * cut_h), int(margin * cut_w)
        cy = np.random.randint(0 + margin_y, img_h - margin_y, size=count)
        cx = np.random.randint(0 + margin_x, img_w - margin_x, size=count)
        yl = np.clip(cy - cut_h // 2, 0, img_h)
        yh = np.clip(cy + cut_h // 2, 0, img_h)
        xl = np.clip(cx - cut_w // 2, 0, img_w)
        xh = np.clip(cx + cut_w // 2, 0, img_w)
        return yl, yh, xl, xh
