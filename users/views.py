from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import CreateUserSerializer, UserSerializer
from polygons.models import ProviderPolygon
from polygons.serializers import (
    CreateProviderPolygonSerializer, ProviderPolygonSerializer
)


class UserView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ProviderPolygonView(CreateAPIView):
    serializer_class = CreateProviderPolygonSerializer
    permission_classes = (AllowAny,)

    def get_serializer_context(self):
        context = super(ProviderPolygonView, self).get_serializer_context()
        # TODO: get user instance through authentication process
        context['user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


class ProviderPolygonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ProviderPolygon.objects.all()
    serializer_class = ProviderPolygonSerializer
    permission_classes = (AllowAny,)
