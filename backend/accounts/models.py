from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="%Y/%m/%d/%H:%M:%S")
    purse = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.username
