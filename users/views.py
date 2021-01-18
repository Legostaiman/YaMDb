from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import CreateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserSerializer, UserSerializerForUser, TokenObtainPairSerializerWithClaims
from .permissions import IsAdmin, IsOwner


class SignUp(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data["email"]
        user = User.objects.create_user(email, email=email)
        send_mail(
            'Cod',
            'Use %s to give your token' % user.confirmation_key,
            'info@yamdb.com',
            ['to@example.com'],
            fail_silently=False,
            )
        return Response(status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializerWithClaims


class AboutMe(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        user = get_object_or_404(User, email=request.user)
        serializer = UserSerializerForUser(user)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, email=request.user)
        serializer = UserSerializerForUser(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Users(APIView, PageNumberPagination):
    permission_classes = [IsAdmin]

    def get(self, request):
        users = User.objects.all()
        results = self.paginate_queryset(users, request, view=self)
        serializer = UserSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView, PageNumberPagination):
    permission_classes = [IsAdmin]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
