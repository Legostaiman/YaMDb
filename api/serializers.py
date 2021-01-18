from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

from .models import Comment, Review, Title, Category, Genre


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    score = serializers.IntegerField(min_value=1, max_value=10)
    
    def validate_author(self, value):

        title_id = self.kwargs.get('title_id')

        title = get_object_or_404(Title, id=title_id)

        if Review.objects.filter(
            author=self.context['request'].user,
            title=title
        ).exists():
            raise serializers.ValidationError()
        return value

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'score')
        model = Review
