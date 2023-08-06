from django.db import models

from flashlearners_core import constants
from .base import BaseModelAbstract


class Question(BaseModelAbstract):
    type = models.CharField(max_length=1, choices=constants.QUESTION_TYPES)
    subject = models.ForeignKey('Subject', models.CASCADE)
    topic = models.ForeignKey('Topic', models.SET_NULL, null=True)
    text = models.TextField(null=True, blank=True)
    image = models.ForeignKey('Media', models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)


class Option(BaseModelAbstract):
    question = models.ForeignKey(Question, models.CASCADE, related_name='options')
    text = models.TextField(null=True, blank=True)
    image = models.ForeignKey('Media', models.CASCADE, null=True, blank=True)
    correct = models.BooleanField(default=False)
