from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import year_validator
from users.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория произведения'
        verbose_name_plural = 'Категории произведений'


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Slug жанра',
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=200
    )
    year = models.IntegerField(
        verbose_name='Год выхода',
        blank=True,
        null=True,
        validators=[year_validator],
    )
    genre = models.ManyToManyField(
        verbose_name='Жанр произведения',
        to=Genre,
        blank=True,
        related_name='titles',

    )
    category = models.ForeignKey(
        Category,
        db_column='category_slug',
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория произведения',
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        max_length=2000,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    score = models.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )

    class Meta:
        ordering = ('-pub_date',)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
