from django.db import models


from .base import BaseModelAbstract


class FlashCard(BaseModelAbstract):
    subject = models.ForeignKey('Subject', models.CASCADE, null=False, blank=False)
    topic = models.ForeignKey('Topic', models.CASCADE, null=False, blank=False)
    question = models.CharField(max_length=255)
    answer = models.TextField(null=False, blank=False)

