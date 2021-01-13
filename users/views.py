from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import CreateView

from .models import User
from .serializers import UserSerializer
#from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class SignUp(CreateView):
    pass
