from django.contrib.auth.models import AbstractUser
from django.db import models

from .base import BaseModelAbstract


class User(AbstractUser, BaseModelAbstract):
    """
        Overrides django's default auth model
    """
    email = None
    last_name = None
    REQUIRED_FIELDS = ["first_name"]

    reset_token = models.CharField(max_length=10, null=True, blank=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)
    avatar = models.ForeignKey('Media', models.SET_NULL, null=True, blank=True)
    current_subscription = models.ForeignKey('Subscription', models.SET_NULL, null=True, blank=True)
