from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from django.core.exceptions import ValidationError

from .models import Comment, Review, Category, Genre, Title


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=request.user
            ).exists():
                raise ValidationError('Review dont be repeated!')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'title_id')


class CommentSerializer(serializers.ModelSerializer):

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializerGet(TitleSerializer):
    rating = serializers.IntegerField(read_only=True, required=False)
    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)


class TitleSerializerPost(TitleSerializer):

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
