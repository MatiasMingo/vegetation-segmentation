import numpy as np
import matplotlib.pyplot as plt
import cv2
import geopandas as gpd
import geoplot
import geoplot.crs as gcrs

def display_image(image, masks)
    #Show segmented tiff and save as jpg
    plt.figure(figsize=(15,25))
    plt.imshow(image)
    all_outlines = show_outlines(masks)
    plt.axis('off')
    plt.savefig('final_segmentation.tiff', bbox_inches='tight')
    plt.show()

def display_geotiff(geotiff_path):
    # Read the created GeoTIFF file
    with rasterio.open(geotiff_path) as src:
        print(src.profile)  # Prints metadata information

    with rasterio.open(geotiff_path) as src:
        plt.imshow(src.read(1))  # Display the first band (adjust as needed)
        plt.show()

def display_geojson(geojson_path):
    data = gpd.read_file(geojson_path)
    geoplot.polyplot(data, projection=gcrs.AlbersEqualArea(), edgecolor='darkgrey', facecolor='lightgrey', linewidth=.3,
    figsize=(12, 8))

def show_outlines(maskgen_data):

    # Bail if there is no mask data
    if len(maskgen_data) == 0:
            return

    # Set up a blank/see-through overlay image, where outlines will be drawn
    ex_mask = maskgen_data[0]["segmentation"]
    img_h, img_w = ex_mask.shape[0:2]
    overlay_img = np.ones((img_h, img_w, 4))
    overlay_img[:,:,3] = 0

    all_outlines = []
    # Generate outlines for each of the maskgen entries
    for each_gen in maskgen_data:

        # Generate outlines based on the boolean mask images
        boolean_mask = each_gen["segmentation"]
        uint8_mask = 255 * np.uint8(boolean_mask)
        mask_contours, _ = cv2.findContours(uint8_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(mask_contours) == 0:
            continue
        all_outlines.append(mask_contours)
        # Draw outlines, using random colors
        outline_opacity = 0.99
        outline_thickness = 2
        outline_color = np.concatenate([[0,0,255], [outline_opacity]])
        cv2.polylines(overlay_img, mask_contours, True, outline_color, outline_thickness, cv2.LINE_AA)

    # Draw the overlay image
    ax = plt.gca()
    ax.set_autoscale_on(False)
    ax.imshow(overlay_img)
    return all_outlines