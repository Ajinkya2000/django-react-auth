from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken

from django.contrib.auth.hashers import make_password

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = RegisterSerializer(self.user).data

        for key, value in serializer.items():
            data[key] = value
        data.pop('refresh', None)
        data.pop('access', None)
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=False, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'username', 'last_name', 'email', 'password', 'token')

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

