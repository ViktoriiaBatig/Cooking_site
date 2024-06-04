from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='static/profile_pics/', blank=True)
    bio = models.TextField(blank=True)
    instagram_url = models.URLField(max_length=255, blank=True, null=True)
    telegram_url = models.CharField(max_length=255, blank=True, null=True)
