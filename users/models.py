import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

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
    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
