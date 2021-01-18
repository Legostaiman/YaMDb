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
