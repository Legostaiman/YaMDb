from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUp, get_token, UserViewSet

router = DefaultRouter()

router.register(
    r'users',
    UserViewSet,
    basename='users'
    )


urlpatterns = [

    path('v1/', include(router.urls)),
    path('v1/auth/email/', SignUp.as_view(), name='confirmation_code'),
    path('v1/auth/token/', get_token, name='token_obtain_pair'),

]
