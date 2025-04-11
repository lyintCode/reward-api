from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    coins = models.IntegerField(default=0)

    def __str__(self):
        return self.username