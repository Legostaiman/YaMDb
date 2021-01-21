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
from django.db.models import Avg

from .models import Comment, Review, Title, Genre, Category
from .permissions import (
    IsOwnerOrReadOnly, 
    IsAdminOrReadOnly, 
    IsModerOrReadOnly,
    IsAdminOrModerOrUser,
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleWriteSerializer,
    TitleReadSerializer,
    GenreSerializer,
    CategorySerializer,
)
from users.models import User
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
        IsAdminOrModerOrUser

    )

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title=title_id).order_by('id')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, 
            title_id=self.kwargs.get('title_id')
        )

    def get_serializer_context(self,):
        return {'title_id': self.kwargs['title_id'],
                'author_id': self.request.user}


class CommentViewSet(viewsets.ModelViewSet,):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrModerOrUser
         )

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


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
        IsAdminOrReadOnly,
    )
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by('-id')
    serializer_class = TitleWriteSerializer
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    )

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleReadSerializer
