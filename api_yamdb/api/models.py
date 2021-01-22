import datetime as dt
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Category(models.Model):
    name = models.CharField(verbose_name='название', max_length=200,
                            unique=True)

    slug = models.SlugField(
        max_length=200,
        unique=True,
    )


class Genre(models.Model):

    name = models.CharField(max_length=200, unique=True)

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
        blank=True,
        related_name='titles',

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

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'


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

    score = models.IntegerField(validators=(
        MinValueValidator(1),
        MaxValueValidator(10))
    )

    class Meta:
        ordering = ('-pub_date', )


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
        ordering = ('-pub_date', )
