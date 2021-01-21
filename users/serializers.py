from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import datetime

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
            'id'
            )
        model = User


class UserSerializerForUser(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
            'id'
            )
        model = User
        read_only_fields = ('role',)


class TokenObtainPairSerializerWithClaims(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        del self.fields['password']
        self.fields['confirmation_key'] = serializers.CharField()


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_key = serializers.CharField(required=True)