from rest_framework import viewsets, permissions
from .serializers import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.all().filter(id=self.request.user.id)


@api_view(['POST'])
def registerUser(request):
    print(12345)
    data = request.data
    print('data', data)
    # data['username'] = data['email']
    # data['password'] = make_password(data['password'])
    serializer = RegisterSerializer(data=data, many=False)
    if serializer.is_valid():
        if User.objects.filter(email=data['email']).exists():
            return Response({"email": ["User with this email Already Exists"]}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)
