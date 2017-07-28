from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import CreateUserSerializer, UserSerializer


class UserView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
