from rest_framework import viewsets, permissions
from .serializers import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.all().filter(id=self.request.user.id)


@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
