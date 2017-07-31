from rest_framework import serializers

from .models import ProviderPolygon
from .utils import (
    get_polygon_obj, build_geometry_json_response, lists_matches
)


class GeometrySerializer(serializers.Serializer):
    type = serializers.CharField()
    coordinates = serializers.ListField(
        child=serializers.ListField(
            child=serializers.ListField(
                child=serializers.IntegerField()
            )
        )
    )

    @staticmethod
    def validate_type(value):
        if value == 'Polygon':
            return value
        raise serializers.ValidationError(
            'The value of this field should be "Polygon".'
        )

    @staticmethod
    def validate_coordinates(value):
        if len(value) is not 1:
            raise serializers.ValidationError(
                'This field should follows GeoJSON object structure.'
            )
        coords_list = value[0]
        if len(coords_list) < 4:
            raise serializers.ValidationError(
                'A Polygon should has at least 4 vertex points.'
            )
        for coord in coords_list:
            if len(coord) is not 2:
                raise serializers.ValidationError(
                    'Every coordinate should has 2 values.'
                )
        if not lists_matches(coords_list[0], coords_list[-1]):
            raise serializers.ValidationError(
                'First and last value coordinates should match.'
            )
        return value


class ProviderPolygonSerializerToWrite(serializers.ModelSerializer):
    geometry = GeometrySerializer(write_only=True)

    class Meta:
        model = ProviderPolygon
        fields = (
            'id', 'name', 'price', 'geometry', 'created_at', 'updated_at'
        )

    def create(self, validated_data):
        polygon_obj = get_polygon_obj(validated_data.pop('geometry'))
        provider_polygon = ProviderPolygon(**dict(
            validated_data,
            geom=polygon_obj,
            user=self.context['user']
        ))
        provider_polygon.save()
        return provider_polygon


class ProviderPolygonSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProviderPolygon
        fields = (
            'id', 'name', 'price', 'geometry', 'created_at', 'updated_at'
        )

    @staticmethod
    def get_geometry(instance):
        return build_geometry_json_response(instance.geom.coords)


class ProviderPolygonWithNameSerializer(ProviderPolygonSerializer):
    provider_name = serializers.SerializerMethodField(read_only=True)

    class Meta(ProviderPolygonSerializer.Meta):
        fields = ProviderPolygonSerializer.Meta.fields + ('provider_name',)

    @staticmethod
    def get_provider_name(value):
        return value.user.name
