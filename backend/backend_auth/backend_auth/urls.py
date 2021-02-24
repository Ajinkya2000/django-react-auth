from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('auth_app.urls'), name='auth'),
    path('api/api-auth/', include('rest_framework.urls')),
]
