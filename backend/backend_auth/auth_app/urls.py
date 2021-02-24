from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserView)

urlpatterns = [
    path('', include(router.urls)),
    path('users/login', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register', registerUser, name='registeruser'),
]
