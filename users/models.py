import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class UserRole:
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        choices = [
            (USER, 'user'),
            (ADMIN, 'admin'),
            (MODERATOR, 'moderator'),
        ]

    role = models.CharField(
        max_length=25,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
