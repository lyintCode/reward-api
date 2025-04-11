from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    coins = models.IntegerField(default=0)
    last_reward_request = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username