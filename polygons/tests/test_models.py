"""Testing models"""

import pytest
from mixer.backend.django import mixer

from ..models import ProviderPolygon
from .test_serializers import TestDataCases

pytestmark = pytest.mark.django_db


class TestProviderPolygon(TestDataCases):
    def test_create_provider_polygon_in_database(self):
        geometries = str(self.data_geometries_valid)
        obj = mixer.blend(
            ProviderPolygon, geom=geometries, pk=1)
        assert obj.pk == 1, 'Should create a polygon in database getting an id'

    def test_create_provider_polygon_instance(self):
        geometries = str(self.data_geometries_valid)
        obj = mixer.blend(
            ProviderPolygon, geom=geometries)
        assert isinstance(obj, ProviderPolygon), (
            'Should create an instance of ProviderPolygon model')
