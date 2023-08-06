import base64

import torch
from torchvision.ops import nms
import numpy as np
import rasterio as rio
import cv2

from mmengine.config import Config
from mmengine.runner import Runner
from shapely.geometry import box
from mmdet.structures import DetDataSample


def rio2patches(img_r, cfg):
    """this function read a rio image and creates patches based on cfg.window and cfg.window.
    return list of patches (patches x window_height x window_width) and list of location of patches (x1, y1, x2, y2).
    Make sure every pixel of image is included in patches. We cannot ignore left and bottom sides.
    Duplicates are okay.
    """
    window_height, window_width = cfg.window if "window" in cfg else (512, 512)

    img_height, img_width = img_r.shape[1], img_r.shape[2]

    if window_height > img_height:
        window_height = img_height

    if window_width > img_width:
        window_width = img_width

    patches = []
    locs = []

    for i in range(0, img_height, window_height):
        for j in range(0, img_width, window_width):
            if img_height < i + window_height:
                y_start = img_height - window_height
                y_end = img_height
            else:
                y_start = i
                y_end = i + window_height

            if img_width < j + window_width:
                x_start = img_width - window_width
                x_end = img_width
            else:
                x_start = j
                x_end = j + window_width

            patch = img_r[:, y_start:y_end, x_start:x_end]

            patches.append(patch)
            locs.append([x_start, y_start])

    return np.array(patches, dtype=np.float32), locs


def merge_seg_patches(mask_patches, location_of_patches):
    """use location of patches to merge logits of patches
    (patches x num_classes x window_height x window_width),
    in case of overlapping area use average of logits.
    After that apply softmax to the num_classes chanel.
    this should return a array of dimension (img_height, img_width)"""

    num_classes = mask_patches.shape[1]
    window_height, window_width = mask_patches.shape[2], mask_patches.shape[3]
    img_height, img_width = (
        location_of_patches[-1][1] + window_height,
        location_of_patches[-1][0] + window_width,
    )

    merged_logits = np.zeros((num_classes, img_height, img_width))
    overlap_count = np.zeros((num_classes, img_height, img_width))

    for i, patch in enumerate(mask_patches):
        x1, y1 = location_of_patches[i]
        x2, y2 = x1 + window_width, y1 + window_height
        merged_logits[:, y1:y2, x1:x2] += patch
        overlap_count[:, y1:y2, x1:x2] += 1

    averaged_merged_logits = merged_logits / overlap_count

    return np.argmax(averaged_merged_logits, axis=0)


def merge_bboxes(bboxes, scores, labels, location_of_patches):
    """This should be easy to merge, the bboxes locations will be localized
    to window_height and window_width, just translate them to original image
    location using location_of_patches. Once all bboxes are merged.
    Use apply non maximal supression, this will remove overlapping boxes area
    due to overlapping regions in patches."""

    flattened_bboxes = []
    flattened_scores = []
    flattened_labels = []

    for i, patch_bbox in enumerate(bboxes):
        x, y = location_of_patches[i]
        for bbox in patch_bbox:
            bbox[0] += x
            bbox[1] += y
            bbox[2] += x
            bbox[3] += y
            flattened_bboxes.append(bbox)
        flattened_scores += scores[i]
        flattened_labels += labels[i]

    if flattened_bboxes:
        keep_idx = nms(
            torch.tensor(flattened_bboxes),
            torch.tensor(flattened_scores),
            iou_threshold=0.5,
        )

        merged_bboxes = np.array(flattened_bboxes)[list(keep_idx.numpy())]
        merged_scores = np.array(flattened_scores)[list(keep_idx.numpy())]
        merged_labels = np.array(flattened_labels)[list(keep_idx.numpy())]

        return merged_bboxes, merged_scores, merged_labels

    return [], [], []


# def classification_as_object_detection(logit_patches, location_of_patches):
#     """This is similar to merge_seg_patches. In case of large images when we apply classification on them.
#        We will be doing that over patches but then we do need to present informatoion for whole image.
#        So all we do is we say that patch is a box. So we create boxes for each patches located in the large images
#        and assign the classification label to it. No need to worry about overlapping regions."""
#     pass


class Inference:
    def __init__(
        self,
        cfg_string,
        weight_file,
        GS_ACCESS_KEY_ID=None,
        GS_SECRET_ACCESS_KEY=None,
        logger=None,
    ):
        cfg = Config.fromstring(cfg_string, file_format=".py")
        cfg.launcher = "none"
        runner = Runner.from_cfg(cfg)

        checkpoint = torch.load(weight_file)
        runner.model.load_state_dict(checkpoint["state_dict"])
        _ = runner.model.eval()

        self.cfg = cfg
        self.runner = runner
        self.GS_ACCESS_KEY_ID = GS_ACCESS_KEY_ID
        self.GS_SECRET_ACCESS_KEY = GS_SECRET_ACCESS_KEY
        self.logger = logger

    def read_raster(self, tif_url):
        try:
            with rio.Env(
                GS_ACCESS_KEY_ID=self.GS_ACCESS_KEY_ID,
                GS_SECRET_ACCESS_KEY=self.GS_SECRET_ACCESS_KEY,
            ):
                r = rio.open(tif_url)
                img = r.read()
            self.logger.info(f"Reading raster {tif_url}")
            return r, img
        except:
            if self.logger:
                self.logger.error(f"Error in reading raster {tif_url}")

    def segmentation(self, tif_path):
        r, img = self.read_raster(tif_path)
        patches, location_of_patches = rio2patches(img, self.cfg)

        window_height, window_width = (
            patches.shape[2],
            patches.shape[3],
        )
        img_height, img_width = img.shape[1], img.shape[2]

        full_mask = np.zeros((img_height, img_width), dtype=np.uint8)

        if self.logger:
            self.logger.info(
                f"Total number of patches for image {tif_path} are: {len(patches)}"
            )

        for i, patch in enumerate(patches):
            model_input = {"inputs": [torch.from_numpy(patch)]}

            result = self.runner.model.test_step(model_input)
            pred_patch = result[0].seg_logits.data.detach().cpu().numpy()
            mask_patch = np.argmax(pred_patch, axis=0)
            mask_patch = np.array(mask_patch, dtype=np.uint8)

            if self.logger:
                self.logger.info(f"Mask Shape: {mask_patch.shape}")

            x1, y1 = location_of_patches[i]
            x2, y2 = x1 + window_width, y1 + window_height
            full_mask[y1:y2, x1:x2] += mask_patch

        patches = []

        is_success, buffer = cv2.imencode(".png", full_mask)
        img_base64 = base64.b64encode(buffer).decode()
        lbl_ids = np.unique(full_mask)

        return img_base64, lbl_ids

    def detection(self, tif_path):
        r, img = self.read_raster(tif_path)
        patches, location_of_patches = rio2patches(img, self.cfg)
        img_shape = (patches.shape[2], patches.shape[3])

        if self.logger:
            self.logger.info(
                f"Total number of patches for image {tif_path} are: {len(patches)}"
            )

        bboxes, scores, labels = [], [], []
        for patch in patches:
            model_input = {
                "inputs": torch.from_numpy(patch).unsqueeze(0),
                "data_samples": [
                    DetDataSample(
                        metainfo={
                            "img_shape": img_shape,
                            "ori_shape": img_shape,
                            "scale_factor": (1, 1),
                        }
                    )
                ],
            }
            result = self.runner.model.test_step(model_input)[0]

            bboxes.append(
                list(result.pred_instances.bboxes.detach().cpu().numpy())
            )
            scores.append(
                list(result.pred_instances.scores.detach().cpu().numpy())
            )
            labels.append(
                list(result.pred_instances.labels.detach().cpu().numpy())
            )
        assert len(bboxes) == len(scores) == len(labels)

        try:
            bboxes, scores, labels = merge_bboxes(
                bboxes, scores, labels, location_of_patches
            )
        except Exception as e:
            if self.logger:
                self.logger.error(e)

        geo_bboxes = []
        for bbox in bboxes:
            x1, y1, x2, y2 = bbox
            xs, ys = rio.transform.xy(r.transform, (y1, y2), (x1, x2))
            poly = box(xs[0], ys[1], xs[1], ys[0])
            geo_bboxes.append([list(poly.exterior.coords)])

        # if self.logger:
        #     self.logger.info(
        #         f"Total number of geo boxes for image {tif_path} are: {len(geo_bboxes)}"
        #     )
        return geo_bboxes, scores, labels

    def classification(self, tif_path):
        pass
