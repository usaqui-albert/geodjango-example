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
    """Service to create and list users

    :accepted_methods:
        POST
        GET
    """
    queryset = User.objects.all().order_by('-id')
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """Rewriting create method to add the token value to the response

        :return: Information of the user with status 201 CREATED
        :except: Message error with status 400 BAD REQUEST
        """
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
    """Service to update and delete a user if this is owner, get request
    is allowed to any user.

    :accepted methods:
        GET
        PUT
        PATCH
        DELETE
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerAccountOrReadOnly,)


class ProviderPolygonView(ListCreateAPIView):
    """Service to add a polygon instance to a user if this is owner, get
    request is allowed to any user

    :accepted methods:
        POST
        GET
    """
    serializer_class = ProviderPolygonSerializer
    permission_classes = (IsOwnerAccountOrReadOnly,)

    def create(self, request, *args, **kwargs):
        """Rewriting create method to pass by context the user which is doing
        the request, only the owner could request.

        :return: Information of the polygon with status 201 CREATED
        :except: Message error with status 400 BAD REQUEST, if the user is not
        owner will receive a message error with status 403 FORBIDDEN
        """
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
        """Method to filter Polygons by user and order from newer to older

        :return: queryset to be used by ProviderPolygonSerializer
        """
        return ProviderPolygon.objects.filter(
            user=self.kwargs['pk']).order_by('-id')


class ProviderPolygonDetailView(RetrieveUpdateDestroyAPIView):
    """Service to update and delete a polygon of a user if this is owner,
    get request is allowed to any user.

    :accepted methods:
        GET
        PUT
        PATCH
        DELETE
    """
    serializer_class = ProviderPolygonSerializerToWrite
    permission_classes = (IsOwnerObjectOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        """Rewriting method to use another serializer(to read)

        :return: Information of the polygon with status 200 OK
        :except: Not found message error with status 404 NOT FOUND
        """
        instance = self.get_object()
        serializer = ProviderPolygonSerializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        """Method to filter Polygon by user

        :return: queryset to be filtered after by pk of Polygon
        """
        return ProviderPolygon.objects.filter(user=self.kwargs['pk_user'])
