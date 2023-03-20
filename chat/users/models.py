from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User class with already implemented username, email and 
    is_active fields from inheritance.
    """
    password = models.CharField(max_length=256)