from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=100)
    tag_type = models.CharField(max_length=50)  # e.g., FLAVOR_PROFILE, INGREDIENT, etc.

    def __str__(self):
        return f"{self.name} ({self.tag_type})"

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    instructions = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="recipes")

    def __str__(self):
        return self.name
    