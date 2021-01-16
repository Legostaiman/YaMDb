from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (
        CommentViewSet, 
        ReviewViewSet, 
        GenreViewSet, 
        CategoryViewSet,
        TitleViewSet 
    )


router = DefaultRouter()

router.register(
    r'titles',
    TitleViewSet,
    basename='title'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/',
    CommentViewSet,
    basename='comment'
)

router.register(
    r'categories',
    CategoryViewSet,
    basename='category'
)

router.register(
    r'genres',
    GenreViewSet,
    basename='genre'
)

urlpatterns = [
    path(
        'api/v1/',
        include(router.urls)
    )
]
