import geopandas as gpd
import rasterio
from rasterio import features


def generate_geojson(mask, geotiff_path, geojson_name):
    with rasterio.open(geotiff_path) as src:
        band=src.read()

        mask = band!= 0
        shapes = features.shapes(band, mask=mask, transform=src.transform)

    fc = ({"geometry": shape, "properties": {"value": value}} for shape, value in shapes)

    gpd.GeoDataFrame.from_features(fc).to_file(f'{geojson_name}.geojson', driver='GeoJSON')