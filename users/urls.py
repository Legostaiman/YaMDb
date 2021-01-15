from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.authtoken import views

from .views import UserViewSet, SignUp

router = DefaultRouter()

router.register(
    r'users',
    UserViewSet,
    basename='user'
    )

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('auth/email/', SignUp, name='confirmation_code'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
