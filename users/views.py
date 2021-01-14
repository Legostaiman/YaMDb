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

from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin, IsOwner


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class SignUp(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.body.email
        user = User.objects.create_user(email, email=email)
        serializer = UserSerializer(data=email)
        if serializer.is_valid():
            serializer.save()
            send_mail(email, 'Use %s to confirm your email' % user.confirmation_key)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AboutMeViewSet(viewsets.ViewSet):
    permission_classes = (IsOwner,)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


#email = 'original@here.com'
#user = User.objects.create_user(email, email=email)
#user.is_confirmed # False

#send_mail(email, 'Use %s to confirm your email' % user.confirmation_key)


#user.confirm_email(user.confirmation_key)
#user.is_confirmed # True
