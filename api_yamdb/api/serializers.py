from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators

from .models import Comment, Review, Category, Genre, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    title = serializers.ReadOnlyField(source='title.name')

    class Meta:
        fields = '__all__'
        model = Review

    def create(self, validated_data):
        title_id = self.context['title_id']
        author_id = self.context['author_id']
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(
                author=author_id,
                title=title
                ).exists():
            raise serializers.ValidationError(
                'Reviews should not be repeated!')
        validated_data['title'] = Title.objects.get(pk=title_id)
        return super(ReviewSerializer, self).create(validated_data)


class CommentSerializer(serializers.ModelSerializer):

    review = serializers.PrimaryKeyRelatedField(read_only=True)
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
