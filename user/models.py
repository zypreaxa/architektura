from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Each tag has a name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)  # Users can have multiple tags