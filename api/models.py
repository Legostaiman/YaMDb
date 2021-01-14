from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import (
    AbstractUser
)
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

User = get_user_model()


class Review(models.Model):

    score = models.IntegerField()

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


class Title(models.Model):

    name = models.CharField(max_length=80,)

    genre = models.CharField(max_length=80,)

    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )
