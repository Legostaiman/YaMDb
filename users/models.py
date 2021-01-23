from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin


class UserManager(UserManager):
    def _create_user(self, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=email, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            username=None,
            email=None,
            password=None,
            **extra_fields
            ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(SimpleEmailConfirmationUserMixin, AbstractUser):

    class Role(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    role = models.TextField(choices=Role.choices, default=Role.USER)
    email = models.EmailField(unique=True, db_index=True)
    bio = models.TextField(blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
