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
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleSerializer,
    GenreSerializer,
    CategorySerializer
    )
from users.models import User


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


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (
        IsOwnerOrReadOnly, 
        permissions.IsAuthenticatedOrReadOnly,
    )
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )

    def get_queryset(self,):
        return Category.objects.all()
  
    def perform_create(self, serializer):
        return serializer.save()
