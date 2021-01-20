from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import (
    filters,
    mixins,
    permissions,
    status,
    viewsets,
)
from rest_framework.views import APIView
from django.http import request
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from .models import Comment, Review, Title, Genre, Category
from .permissions import IsOwnerOrReadOnly,\
    IsAdmin,\
    IsSuperUserOrReadOnly,\
    TitlePermission

from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    CategorySerializer,
    GenreSerializer,
    CategorySerializer,
    ReviewSerializer,
    TitleSerializerPost,
    TitleSerializerGet,
)

from users.models import User
from .pagination import CustomPagination
from rest_framework.permissions import SAFE_METHODS


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


class CommentViewSet(viewsets.ModelViewSet):
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
        return reviews.comments.all().order_by('id')  # Спросить. post.comoents.all().order_by('id')


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUserOrReadOnly,]
    pagination_class = CustomPagination
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    serializer_class = GenreSerializer
    permission_classes = [IsSuperUserOrReadOnly,]
    pagination_class = CustomPagination
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = [filters.SearchFilter]
    #search_fields = ['name']
    permission_classes = [TitlePermission,]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleSerializerGet
        return TitleSerializerPost

    def get_queryset(self):
        queryset = Title.objects.all()
        genre = self.request.query_params.get('genre', None)
        if genre is not None:
            queryset = Title.objects.filter(
                genre=Genre.objects.get(slug=genre))
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = Title.objects.filter(
                category=Category.objects.get(slug=category))
        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = Title.objects.filter(
                year=year)
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = Title.objects.filter(
                name__contains=name)
        return queryset












'''    def get_queryset(self,):
        return Category.objects.all()
  
    def perform_create(self, serializer):
        return serializer.save()
'''