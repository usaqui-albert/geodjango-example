from django.conf.urls import url

from .views import ProviderPolygonByLocationView


urlpatterns = [
    url(r'^$', ProviderPolygonByLocationView.as_view()),
]
