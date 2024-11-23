from django.db import models
from django.contrib.auth.models import User
from nlp.models import Tag

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_cuisine = models.CharField(max_length=100)
    preferred_recipe_type = models.CharField(max_length=100)
    
    soft_tags = models.ManyToManyField(Tag, related_name="user_profiles_soft")
    strict_tags = models.ManyToManyField(Tag, related_name="user_profiles_strict")
    
    def __str__(self):
        return f"{self.user_profile} - {self.tag}"