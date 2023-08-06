from django.db import models
from .base import BaseModelAbstract


class Media(BaseModelAbstract):
    url = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    is_local = models.BooleanField(default=True)


class Video(BaseModelAbstract):
    subject = models.ForeignKey('Subject', models.CASCADE, null=False, blank=False)
    topic = models.ForeignKey('Topic', models.CASCADE, null=False, blank=False)
    media = models.ForeignKey('Media', models.CASCADE)
    duration = models.IntegerField(null=False, blank=False)
