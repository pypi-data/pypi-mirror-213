from django.db import models

from flashlearners_core import constants
from .base import BaseModelAbstract


class Guide(BaseModelAbstract):
    type = models.CharField(max_length=1, choices=constants.GUIDE_TYPES)
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(null=False, blank=False)


class Novel(BaseModelAbstract):
    type = models.CharField(max_length=1, default=0)
    title = models.CharField(max_length=100, null=False, blank=False)


class NovelChapter(BaseModelAbstract):
    novel = models.ForeignKey('Novel', models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
