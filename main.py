"""
!pip install git+https://github.com/facebookresearch/segment-anything.git
!pip install opencv-python pycocotools matplotlib onnxruntime onnx
"""

"""
using_colab = True

if using_colab:
    import torch
    import torchvision
    print("PyTorch version:", torch.__version__)
    print("Torchvision version:", torchvision.__version__)
    print("CUDA is available:", torch.cuda.is_available())
    import sys
    !{sys.executable} -m pip install opencv-python matplotlib
    !{sys.executable} -m pip install 'git+https://github.com/facebookresearch/segment-anything.git'

    !mkdir images
    !wget -P images https://raw.githubusercontent.com/facebookresearch/segment-anything/main/notebooks/images/dog.jpg

    !wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
"""

import sam_interaction
import display_images
import files_interaction


if __name__ == "__main__":
    mask_generator = sam_interaction.load_model()
    geotiff_path = "resources/geo_tiffs/vegetation.tiff"
    masks = sam_interaction.predict_masks(mask_generator, geotiff_path)
    files_interaction.generate_geojson(masks, geotiff_path, "vegetation")