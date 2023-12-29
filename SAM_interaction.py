import cv2
import sys
#sys.path.append("..")
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

def load_model():
    sam_checkpoint = "sam_vit_h_4b8939.pth"
    model_type = "vit_h"
    #device = "cuda"
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    #sam.to(device=device)
    mask_generator = SamAutomaticMaskGenerator(
        model=sam,
        points_per_side=32,
        pred_iou_thresh=0.86,
        stability_score_thresh=0.95,
        crop_n_layers=1,
        crop_n_points_downscale_factor=20,
        min_mask_region_area=100
    )
    return mask_generator

def predict_masks(mask_generator, geotiff_path):
    image = cv2.imread(geotiff_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    masks = mask_generator.generate(image)
    return masks