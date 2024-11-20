from django.db import models
from django.contrib.auth.models import User

# Tag model that can be used to label or categorize users
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

# Custom join table model for Many-to-Many relationship
class UserTag(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # Additional field can be added to the join table if needed
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_profile', 'tag')  # Ensure each (user_profile, tag) pair is unique

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.tag.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_cuisine = models.CharField(max_length=100)
    preferred_recipe_type = models.CharField(max_length=100)

