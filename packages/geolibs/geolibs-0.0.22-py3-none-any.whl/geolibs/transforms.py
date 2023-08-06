import numpy as np 

import mmcv 

from mmcv.transforms import BaseTransform
from mmengine.registry import TRANSFORMS


@TRANSFORMS.register_module()
class ResizeAllToThisBand(BaseTransform):
    """Resize all bands to a given band size and make a tensor.

    Args:
        keys (list): band keys.
        band_to_use (str): band key to use for the destination shape.
        interpolation (str): Interpolation method. For "cv2" backend, accepted
            values are "nearest", "bilinear", "bicubic", "area", "lanczos". For
            "pillow" backend, accepted values are "nearest", "bilinear",
            "bicubic", "box", "lanczos", "hamming".
            More details can be found in `mmcv.image.geometric`.
        backend (str): The image resize backend type, accepted values are
            `cv2` and `pillow`. Default: `cv2`.
    """

    def __init__(self,
                 keys,
                 band_to_use,
                 interpolation='bilinear',
                 backend='cv2'):
        
        if backend not in ['cv2', 'pillow']:
            raise ValueError(f'backend: {backend} is not supported for resize.'
                             'Supported backends are "cv2", "pillow"')
        if backend == 'cv2':
            assert interpolation in ('nearest', 'bilinear', 'bicubic', 'area',
                                     'lanczos')
        else:
            assert interpolation in ('nearest', 'bilinear', 'bicubic', 'box',
                                     'lanczos', 'hamming')
        self.keys = keys
        self.band_to_use = band_to_use
        self.interpolation = interpolation
        self.backend = backend

    def _resize_bands(self, results):
        h, w = results[self.band_to_use].shape[1:]
        img = []
        for key in self.keys:
            band = results[key]
            img.append(mmcv.imresize(
                    band[0],
                    size=(w, h),
                    interpolation=self.interpolation,
                    return_scale=False,
                    backend=self.backend))
        img = np.asarray(img).transpose(1, 2, 0)
        results['img'] = img
        results['img_shape'] = img.shape[:2]
        results['ori_shape'] = img.shape[:2]

        for key in self.keys:
            del results[key]

    def transform(self, results):
        self._resize_bands(results)
        return results

    def __repr__(self):
        repr_str = self.__class__.__name__
        repr_str += f'(size={self.size}, '
        repr_str += f'interpolation={self.interpolation})'
        return repr_str