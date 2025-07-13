import pytest
from django.test import TestCase
from apps.core.models import User, UserProfile


class TestUserAndProfile(TestCase):
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username='john', email='john@example.com', password='pass')
        profile = UserProfile.objects.get(user=user)
        assert profile.user == user

    def test_profile_deleted_with_user(self):
        user = User.objects.create_user(username='jane', email='jane@example.com', password='pass')
        user_id = user.id
        user.delete()
        assert not UserProfile.objects.filter(user_id=user_id).exists()
