from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    mail = models.EmailField(
        max_length=255,
        unique=True
    )
    password = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.mail
