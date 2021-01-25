from rest_framework import (
    filters,
    mixins,
    permissions,
    viewsets,
)
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework.permissions import SAFE_METHODS

from .models import (
    Review,
    Title,
    Genre,
    Category
)
from .permissions import (
    ReviewCommentPermission,
    IsSuperUserOrReadOnly
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleSerializerGet,
    TitleSerializerPost
)
from .filters import TitleFilter


class CDLViewSet(
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
        ReviewCommentPermission
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet,):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ReviewCommentPermission
    )

    def get_queryset(self):
        reviews = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return reviews.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class GenreViewSet(CDLViewSet):
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    serializer_class = GenreSerializer
    permission_classes = (IsSuperUserOrReadOnly, )
    lookup_field = 'slug'


class CategoryViewSet(CDLViewSet):
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
