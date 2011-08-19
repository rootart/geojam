import os
from django.contrib.gis.utils import LayerMapping
from core.models import Administrative

mapping = {
    'name' : 'NAME',
    'admin_level': 'ADMIN_LEVE',
    'geodata' : 'LINESTRING',
}

shape_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/ukraine_administrative.shp'))

def run(verbose=True):
    lm = LayerMapping(Administrative, shape_file, mapping,
        transform=False, encoding='UTF-8')

    lm.save(strict=True, verbose=verbose)