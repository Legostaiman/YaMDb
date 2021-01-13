from django.urls import path, include
from rest_framework.authtoken import views

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
        )

from .views import CommentViewSet, ReviewViewSet


router = DefaultRouter()

router.register(
    'titles/{title_id}/reviews/{review_id}/',
    ReviewViewSet,
    basename='review'
)

router.register(
    'comments/{comment_id}',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path(
        'api/v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    path(
        'v1/',
        include(router.urls)
    ),
]
