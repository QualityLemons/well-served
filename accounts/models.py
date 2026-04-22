from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Use email as the primary identifier
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email and Password are required by default

    def __str__(self):
        return self.email