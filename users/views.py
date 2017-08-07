from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import CreateUserSerializer, UserSerializer

from moziotest.permissions import (
    IsOwnerAccountOrReadOnly, IsOwnerObjectOrReadOnly
)

from polygons.models import ProviderPolygon
from polygons.serializers import (
    ProviderPolygonSerializerToWrite, ProviderPolygonSerializer
)


class UserView(ListCreateAPIView):
    queryset = User.objects.all().order_by('-id')
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            dict(serializer.data, token=str(user.auth_token)),
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerAccountOrReadOnly,)


class ProviderPolygonView(ListCreateAPIView):
    serializer_class = ProviderPolygonSerializer
    permission_classes = (IsOwnerAccountOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = ProviderPolygonSerializerToWrite(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def get_queryset(self):
        return ProviderPolygon.objects.filter(
            user=self.kwargs['pk']).order_by('-id')


class ProviderPolygonDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProviderPolygonSerializerToWrite
    permission_classes = (IsOwnerObjectOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProviderPolygonSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        return ProviderPolygon.objects.filter(user=self.kwargs['pk_user'])
