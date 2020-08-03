from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Address(models.Model):
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_online = models.BooleanField()
    last_checked = models.DateTimeField(default=timezone.now())
