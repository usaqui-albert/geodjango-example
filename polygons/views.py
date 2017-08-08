from django.contrib.gis.geos import Point

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import ProviderPolygon
from .serializers import ProviderPolygonWithNameSerializer


class ProviderPolygonByLocationView(ListAPIView):
    """Service to get the list of Polygons given a lat lng values by query
    params, otherwise will return a list of all polygons with pagination

    :accepted methods:
        GET
    """
    serializer_class = ProviderPolygonWithNameSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """Method to filter by a Point(lat, lng) and prefetching(JOIN) the
        user owner of the polygon (provider)

        :return: queryset to be used by ProviderPolygonWithNameSerializer
        """
        queryset = ProviderPolygon.objects.all().select_related(
            'user').order_by('id')
        query_params = self.request.query_params
        lat = query_params.get('lat', None)
        lng = query_params.get('lng', None)
        if lat and lng:
            point = Point(int(lat), int(lng))
            return queryset.filter(geom__contains=point)
        return queryset
