import datetime as dt
from django.db import models
from django.core.validators import MaxValueValidator

from users.models import User


class Review(models.Model):
    text = models.TextField(null=False, max_length=2000)

    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    post = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    text = models.TextField()

    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)


class Category(models.Model):
    name = models.CharField(verbose_name='название', max_length=200,
                            unique=True)

    slug = models.SlugField(
        max_length=200,
        unique=True,
    )


class Genre(models.Model):
    name = models.CharField(verbose_name='название', max_length=200)

    slug = models.SlugField(
        max_length=200,
        unique=True,
    )


class Title(models.Model):
    name = models.CharField(verbose_name='название', max_length=200)

    year = models.IntegerField(
        verbose_name='год',
        blank=True,
        null=True,
        validators=[MaxValueValidator(dt.date.today().year)],
    )

    genre = models.ManyToManyField(
        to=Genre,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        db_column='category_slug',
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        blank=True,
        null=True,
    )

    description = models.TextField(
        verbose_name='описание',
        max_length=2000,
        blank=True,
    )

    rating = models.IntegerField(
        verbose_name='рейтинг',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
