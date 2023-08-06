from django.db import models

from .base import BaseModelAbstract


class Topic(BaseModelAbstract):
    subject = models.ForeignKey('Subject', models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    notes = models.TextField()
    allow_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
