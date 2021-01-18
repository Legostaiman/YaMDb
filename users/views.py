from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import UserSerializer, UserSerializerForUser,\
    ConfirmationCodeSerializer
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


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    error_message = 'confirmation key is not valid'
    serializer = ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_key = serializer.data.get('confirmation_key')
        user = get_object_or_404(User, email=email)
        if confirmation_key == user.confirmation_key:
            token = AccessToken.for_user(user)
            user.is_active = True
            user.save
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_key': f'{error_message}'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


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
