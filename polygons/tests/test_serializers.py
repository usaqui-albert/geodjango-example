"""Testing serializers"""

import pytest
from mixer.backend.django import mixer

from .. import serializers
from ..models import ProviderPolygon

pytestmark = pytest.mark.django_db


class TestDataCases(object):

    data_geometries_type_not_polygon = {
        'type': 'Point',
        'coordinates': [
            [
                [0, 0],
                [0, 50],
                [50, 50],
                [50, 0],
                [0, 0]
            ]
        ]
    }

    data_geometries_coordinates_should_be_a_list = {
        'type': 'Polygon',
        'coordinates': {}
    }

    data_geometries_coordinates_child_should_be_a_list = {
        'type': 'Polygon',
        'coordinates': [
            {}
        ]
    }

    data_geometries_coordinates_length_should_be_1 = {
        'type': 'Polygon',
        'coordinates': [
            [],
            []
        ]
    }

    data_geometries_coordinates_grandchild_should_be_list = {
        'type': 'Polygon',
        'coordinates': [
            [
                2,
                {}
            ]
        ]
    }

    data_geometries_coordinates_at_least_4_vertex_points = {
        'type': 'Polygon',
        'coordinates': [
            [
                [],
                [],
                []
            ]
        ]
    }

    data_geometries_vertex_points_should_have_2_values = {
        'type': 'Polygon',
        'coordinates': [
            [
                [],
                [0, 50, 0],
                [50],
                [0]
            ]
        ]
    }

    data_geometries_first_and_last_coordinates_should_match = {
        'type': 'Polygon',
        'coordinates': [
            [
                [0, 0],
                [0, 50],
                [50, 50],
                [50, 0]
            ]
        ]
    }

    data_geometries_valid = {
        'type': 'Polygon',
        'coordinates': [
            [
                [0, 0],
                [0, 50],
                [50, 50],
                [50, 0],
                [0, 0]
            ]
        ]
    }


class TestGeometrySerializer(TestDataCases):
    serializer_class = serializers.GeometrySerializer

    def test_is_valid_type_not_polygon(self):
        serializer = self.serializer_class(
            data=self.data_geometries_type_not_polygon)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_type_not_polygon(self):
        serializer = self.serializer_class(
            data=self.data_geometries_type_not_polygon)
        serializer.is_valid()
        assert 'type' in serializer.errors, 'Should has type key'
        error_message = 'The value of this field should be "Polygon".'
        assert error_message in serializer.errors['type']

    def test_is_valid_coordinates_should_be_a_list(self):
        serializer = self.serializer_class(
            data=self.data_geometries_coordinates_should_be_a_list)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_coordinates_should_be_a_list(self):
        serializer = self.serializer_class(
            data=self.data_geometries_coordinates_should_be_a_list)
        serializer.is_valid()
        assert 'coordinates' in serializer.errors
        error_message = 'Expected a list of items but got type "dict".'
        assert error_message in serializer.errors['coordinates']

    def test_is_valid_coordinates_child_should_be_a_list(self):
        serializer = self.serializer_class(
            data=self.data_geometries_coordinates_child_should_be_a_list)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_coordinates_child_should_be_a_list(self):
        serializer = self.serializer_class(
            data=self.data_geometries_coordinates_child_should_be_a_list)
        serializer.is_valid()
        assert 'coordinates' in serializer.errors
        error_message = 'Expected a list of items but got type "dict".'
        assert error_message in serializer.errors['coordinates']

    def test_is_valid_coordinates_length_should_be_1(self):
        serializer = self.serializer_class(
            data=self.data_geometries_coordinates_length_should_be_1)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_coordinates_length_should_be_1(self):
        serializer = self.serializer_class(
            data=self.data_geometries_coordinates_length_should_be_1)
        serializer.is_valid()
        assert 'coordinates' in serializer.errors
        error_message = 'This field should follows GeoJSON object structure.'
        assert error_message in serializer.errors['coordinates']

    def test_is_valid_coordinates_grandchild_should_be_list(self):
        serializer = self.serializer_class(
            data=self.data_geometries_coordinates_grandchild_should_be_list)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_coordinates_grandchild_should_be_list(self):
        serializer = self.serializer_class(
            data=self.data_geometries_coordinates_grandchild_should_be_list)
        serializer.is_valid()
        assert 'coordinates' in serializer.errors
        error_message = 'Expected a list of items but got type "int".'
        assert error_message in serializer.errors['coordinates']

    def test_is_valid_coordinates_at_least_4_vertex_points(self):
        serializer = self.serializer_class(
            data=self.data_geometries_coordinates_at_least_4_vertex_points)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_coordinates_at_least_4_vertex_points(self):
        serializer = self.serializer_class(
            data=self.data_geometries_coordinates_at_least_4_vertex_points)
        serializer.is_valid()
        assert 'coordinates' in serializer.errors
        error_message = 'A Polygon should has at least 4 vertex points.'
        assert error_message in serializer.errors['coordinates']

    def test_is_valid_vertex_points_should_have_2_values(self):
        serializer = self.serializer_class(
            data=self.data_geometries_vertex_points_should_have_2_values)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_vertex_points_should_have_2_values(self):
        serializer = self.serializer_class(
            data=self.data_geometries_vertex_points_should_have_2_values)
        serializer.is_valid()
        assert 'coordinates' in serializer.errors
        error_message = 'Every coordinate should has 2 values.'
        assert error_message in serializer.errors['coordinates']

    def test_is_valid_first_and_last_coordinates_should_match(self):
        serializer = self.serializer_class(
            data=self.data_geometries_first_and_last_coordinates_should_match)
        assert not serializer.is_valid(), 'Should not be a valid data'

    def test_errors_message_first_and_last_coordinates_should_match(self):
        serializer = self.serializer_class(
            data=self.data_geometries_first_and_last_coordinates_should_match)
        serializer.is_valid()
        assert 'coordinates' in serializer.errors
        error_message = 'First and last value coordinates should match.'
        assert error_message in serializer.errors['coordinates']
