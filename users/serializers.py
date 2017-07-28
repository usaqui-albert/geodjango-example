from rest_framework.serializers import ModelSerializer

from .models import User


class CreateUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'name', 'phone_number', 'language',
            'currency', 'created_at', 'updated_at',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'name', 'phone_number', 'language', 'currency',
            'created_at', 'updated_at',
        )
