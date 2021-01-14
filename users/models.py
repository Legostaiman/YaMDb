from django.contrib.auth.models import (
    AbstractUser
)
from django.db import models

from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin


class User(SimpleEmailConfirmationUserMixin, AbstractUser):

    class Role(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    role = models.TextField(choices=Role.choices, default=Role.USER)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
