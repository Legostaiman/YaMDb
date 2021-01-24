from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators

from .models import Comment, Review, Category, Genre, Title


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'title_id')

    def validate(self, attrs):
        if self.context.get('request').method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            user = self.context.get('request').user
            if Review.objects.filter(title_id=title_id, author=user).exists():
                raise serializers.ValidationError(
                    'Вы уже написали ревью на это произведение'
                )
        return attrs


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    
    class Meta:
        model = Comment
        exclude = ('review_id', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',
                  'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',
                  'slug')


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
    