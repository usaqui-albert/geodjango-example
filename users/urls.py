from django.conf.urls import url

from .views import (
    UserView, UserDetailView, ProviderPolygonView, ProviderPolygonDetailView
)

urlpatterns = [
    url(r'^$', UserView.as_view()),
    url(r'^/(?P<pk>\d+)$', UserDetailView.as_view()),
    url(r'^/(?P<pk>\d+)/polygons$', ProviderPolygonView.as_view()),
    url(r'^/(?P<pk_user>\d+)/polygons/(?P<pk>\d+)$',
        ProviderPolygonDetailView.as_view()),
]
