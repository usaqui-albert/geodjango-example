from django.contrib.gis.geos import GEOSGeometry


def get_polygon_obj(polygon_data):
    data = dict(polygon_data)
    polygon_obj = GEOSGeometry(str(data), srid=4326)
    return polygon_obj


def build_geometry_json_response(coords):
    return {
        'type': 'Polygon',
        'coordinates': coords
    }


def lists_matches(list_x, list_y):
    for value_x, value_y in zip(list_x, list_y):
        if value_x is not value_y:
            return False
    return True
