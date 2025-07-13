from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with unique email."""
    email = models.EmailField(unique=True)


class UserProfile(models.Model):
    """Profile model linked to :class:`User`."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"Profile of {self.user.username}"


# Automatically create a profile when a user is created
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
