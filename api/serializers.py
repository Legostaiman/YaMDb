from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Review, User, Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = ('id', 'score', 'author', 'text', 'created')
        model = Review


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'pub_date', 'genre')
        model = Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User