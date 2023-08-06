from django.db import models

from flashlearners_core import constants
from .base import BaseModelAbstract


class Faq(BaseModelAbstract):
    type = models.CharField(max_length=1, choices=constants.FAQ_TYPES)
    answer = models.TextField(null=False, blank=False)
