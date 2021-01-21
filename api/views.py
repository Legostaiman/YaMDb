from rest_framework import (
    filters,
    mixins,
    permissions,
    viewsets,
)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from django.db.models import Avg
from rest_framework.permissions import SAFE_METHODS

from .models import (
    Comment,
    Review,
    Title,
    Genre,
    Category,
)
from .permissions import (
    IsAdminOrReadOnly,
    ReviewCommentPermission,
    IsSuperUserOrReadOnly,
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleSerializer,
    TitleSerializerGet,
    TitleSerializerPost,
)
from .filters import TitleFilter
from users.models import User


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
        ReviewCommentPermission,
    )

    def get_queryset(self):
        title = self.kwargs['title_id']
        return Review.objects.filter(title=title).order_by('id')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.kwargs.get('title_id')
        )

    def get_serializer_context(self,):
        return {'title_id': self.kwargs['title_id'],
                'author_id': self.request.user}


class CommentViewSet(viewsets.ModelViewSet,):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ReviewCommentPermission,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    serializer_class = GenreSerializer
    permission_classes = (IsSuperUserOrReadOnly, )
    lookup_field = 'slug'


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    serializer_class = CategorySerializer
    permission_classes = (IsSuperUserOrReadOnly, )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-id')
    filter_backends = (DjangoFilterBackend, )
    permission_classes = (IsSuperUserOrReadOnly, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleSerializerGet
        return TitleSerializerPost
