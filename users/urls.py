from django.conf.urls import url

from .views import UserView, UserDetailView

urlpatterns = [
    url(r'^$', UserView.as_view()),
    url(r'^/(?P<pk>\d+)$', UserDetailView.as_view()),
]
