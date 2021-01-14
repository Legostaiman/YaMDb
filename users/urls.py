from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserViewSet, SignUp, AboutMeViewSet

router = DefaultRouter()

router.register(
    r'users/me',
    AboutMeViewSet,
    basename='about_me'
    )

router.register(
    r'users',
    UserViewSet,
    basename='user'
    )


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('auth/email/', SignUp.as_view(), name='confirmation_code'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
