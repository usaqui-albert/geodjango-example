from django.conf.urls import url

from .views import ProviderPolygonByLLView


urlpatterns = [
    url(r'^$', ProviderPolygonByLLView.as_view()),
]
