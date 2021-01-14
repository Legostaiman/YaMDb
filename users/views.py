from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import CreateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail

from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser, IsAdmin]


class SignUp(APIView):
    def post(self, request):
        email = request.data.email
        user = User.objects.create_user(email, email=email)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_mail(email, 'Use %s to confirm your email' % user.confirmation_key)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#email = 'original@here.com'
#user = User.objects.create_user(email, email=email)
#user.is_confirmed # False

#send_mail(email, 'Use %s to confirm your email' % user.confirmation_key)


#user.confirm_email(user.confirmation_key)
#user.is_confirmed # True
