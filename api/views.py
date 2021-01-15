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

<<<<<<< HEAD
from .models import Comment, Review, Title
=======
from .models import Comment, Review, User, Title
>>>>>>> Andrey_branch3
from .permissions import IsOwnerOrReadOnly, IsAdmin
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    TitleSerializer,
<<<<<<< HEAD
    )
from users.models import User
=======
    UserSerializer
    )
>>>>>>> Andrey_branch3


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = (
        IsOwnerOrReadOnly,
    )
    serializer_class = ReviewSerializer

    def get_quryset(self):
        post = get_object_or_404(Review, pk=self.kwargs.get('title_id'))
        return post.reviews.all()


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
    filter_backends = (filters.SearchFilter)
    search_fields = ['year',]
    serializer_class = TitleSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    )
    queryset = Title.objects.all()

    def get_queryset(self):
        post = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return post.titles.all()
