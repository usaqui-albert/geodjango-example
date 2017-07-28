from django.contrib.gis.db import models

from users.models import User


class ProviderPolygon(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, related_name='polygons')
    geom = models.PolygonField(srid=4326)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
