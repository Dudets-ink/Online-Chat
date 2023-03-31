from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User class inherits username, email and 
    is_active fields from AbstractUser.
    """
    password = models.CharField(max_length=256)