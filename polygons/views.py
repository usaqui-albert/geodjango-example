from django.contrib.gis.geos import Point

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import ProviderPolygon
from .serializers import ProviderPolygonWithNameSerializer


class ProviderPolygonByLocationView(ListAPIView):
    serializer_class = ProviderPolygonWithNameSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = ProviderPolygon.objects.all().select_related(
            'user').order_by('id')
        query_params = self.request.query_params
        lat = query_params.get('lat', None)
        lng = query_params.get('lng', None)
        if lat and lng:
            point = Point(int(lat), int(lng))
            return queryset.filter(geom__contains=point)
        return queryset
