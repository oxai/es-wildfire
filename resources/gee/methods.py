import ee
from .products import EE_PRODUCTS
from . import cloud_mask as cm
from . import vis_handler
from .vis_handler import default_vis_handler
from ..utils.gis import get_bbox_corners_for_tile, get_tile_pixel_scale_from_zoom


def image_to_map_id(ee_image, vis_params=None):
    """
    Get map_id parameters
    """
    if vis_params is None:
        vis_params = {}
    map_id = ee_image.getMapId(vis_params)
    map_id_params = {
        'mapid': map_id['mapid'],
        'token': map_id['token']
    }
    return map_id_params


def get_ee_product(platform, sensor, product):
    return EE_PRODUCTS[platform][sensor][product]


def get_ee_product_name(ee_product):
    return ee_product['collection'].replace('/', '-')


def get_ee_image_from_product(ee_product, date_from, date_to, reducer='median'):
    """
    Get tile url for image collection asset.
    """
    if not date_from or not date_to:
        raise Exception("Too many images to handle. Define data_from and date_to")

    collection = ee_product['collection']
    cloud_mask = ee_product.get('cloud_mask', None)

    ee_collection = ee.ImageCollection(collection)\
        .filter(
            ee.Filter.date(date_from, date_to)
        )

    if cloud_mask:
        cloud_mask_func = getattr(cm, cloud_mask, None)
        if cloud_mask_func:
            ee_collection = ee_collection.map(cloud_mask_func)

    ee_image = getattr(ee_collection, reducer)()

    return ee_image


def get_map_tile_url(ee_image, vis_params=None):
    tile_url_template = "https://earthengine.googleapis.com/v1alpha/{mapid}/tiles/{{z}}/{{x}}/{{y}}"
    map_id_params = image_to_map_id(ee_image, vis_params)
    return tile_url_template.format(**map_id_params)


def get_image_download_url(ee_image, bbox, scale, name=None):
    name = {'name': name} if name else {}
    geometry = ee.Geometry.Rectangle(bbox)

    return ee_image.getDownloadURL({
        **name,
        "scale": scale,
        'crs': 'EPSG:3857',     # WGS 84 Web Mercator
        "region": geometry["coordinates"]
    })


def get_image_download_url_for_tile(ee_image, x_tile, y_tile, zoom, name=None):
    bbox = get_bbox_corners_for_tile(x_tile, y_tile, zoom)
    scale = get_tile_pixel_scale_from_zoom(zoom)
    return get_image_download_url(ee_image, bbox, scale, name)


def visualise_image(ee_product, image, method='default'):
    vis_params = ee_product['vis_params']
    if method == 'default':
        return default_vis_handler(ee_product, image, vis_params)
    handler_name = vis_params['handler'][method]
    handler = getattr(vis_handler, handler_name, None)
    if not handler:
        raise Exception(f"No definition provided for visualizer: {handler_name}")
    return handler(ee_product, image, vis_params)