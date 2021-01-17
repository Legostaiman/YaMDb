from django.shortcuts import render
from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    viewsets,
)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from .models import Comment, Review, Title, Genre, Category
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleSerializer,
    GenreSerializer,
    CategorySerializer
    )
from users.models import User
from users.permissions import IsAdmin
from .filters import TitleFilter


class CustomViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, 
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer, *args, **kwargs):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        if not Review.objects.filter(author=self.request.user,
                                     title=title).exists():
            serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet,):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        post = get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
        return reviews.comments.all().order_by('id')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_class = TitleFilter


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    )
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
