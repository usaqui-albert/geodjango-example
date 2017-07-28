from rest_framework import serializers

from .models import ProviderPolygon
from .utils import get_polygon_obj, build_geometry_json_response


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
        raise serializers.ValidationError('Geometry type should be Polygon.')


class CreateProviderPolygonSerializer(serializers.ModelSerializer):
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
