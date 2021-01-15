import datetime as dt
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import (
    AbstractUser
)
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from django.core.validators import MaxValueValidator

from users.models import User


class Review(models.Model):
    text = models.TextField(null=False,)

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
    name = models.CharField(verbose_name='название', max_length=200)

    slug = models.SlugField(max_length=200, unique=True,)


class Genre(models.Model):
    name = models.CharField(verbose_name='название', max_length=200)

    slug = models.SlugField(max_length=200, unique=True,)


class Title(models.Model):
    name = models.CharField(verbose_name='название', max_length=200)

    year = models.IntegerField(
        verbose_name='год',
        blank=True,
        null=True,
        validators=[MaxValueValidator(dt.date.today().year)],
    )

    rating = models.IntegerField(
        verbose_name='рейтинг',
        blank=True,
        null=True,
    ) 

    description = models.TextField(
        verbose_name='описание',
        max_length=2000,
        blank=True,
    )

    genre = models.ManyToManyField(
        to=Genre,
        related_name='titles',
        blank=True,
        verbose_name='жанры',
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
