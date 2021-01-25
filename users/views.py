from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters

from .models import User
from .serializers import (
    UserSerializer,
    SignUpSerializer,
    UserSerializerForUser,
    ConfirmationCodeSerializer
    )
from .permissions import IsAdmin, IsOwner


class SignUp(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.create_user(email, email=email)
        send_mail(
            'Cod',
            'Use %s to give your token' % user.confirmation_key,
            settings.ADMINS_EMAIL,
            [email],
            fail_silently=False,
            )
        return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    error_message = 'confirmation key is not valid'
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    confirmation_key = serializer.validated_data.get('confirmation_key')
    user = get_object_or_404(User, email=email)
    if confirmation_key == user.confirmation_key:
        token = AccessToken.for_user(user)
        user.is_active = True
        user.save
        return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
    return Response({'confirmation_key': f'{error_message}'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    lookup_value_regex = r'[^/]+'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated, IsOwner]
        )
    def me(self, request):
        if request.method == "GET":
            serializer = UserSerializerForUser(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = UserSerializerForUser(
                request.user,
                data=request.data,
                partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
