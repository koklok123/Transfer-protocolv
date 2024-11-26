from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import UsersApi, UserCreateAPIView
    
# Роутер для ViewSet
router = DefaultRouter()
router.register(r'users', UsersApi, basename='users')

urlpatterns = [
    path('', include(router.urls)),  # Маршруты от роутера
    path('register/', UserCreateAPIView.as_view(), name='user_register'),

    # JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
