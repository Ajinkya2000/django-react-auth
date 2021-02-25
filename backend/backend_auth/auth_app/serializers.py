from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, RefreshToken


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #
    #     # Add custom claims
    #     token['username'] = user.username
    #     # token['message'] = "You can send as many details as you want like this in the token."
    #
    #     return token

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        for key, value in serializer.items():
            data[key] = value

        # data['username'] = self.user.username
        # data['email'] = self.user.email

        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=300, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'email', 'token')

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
