from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.common.services.user_service import UserService

User = get_user_model()


class TestUserService(TestCase):
    def setUp(self):
        self.service = UserService()
        self.user1 = User.objects.create_user(
            username='user1', email='user1@example.com', password='pass', is_active=True
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@example.com', password='pass', is_active=False
        )
        self.staff = User.objects.create_user(
            username='staff', email='staff@example.com', password='pass', is_staff=True
        )

    def test_get_active_users(self):
        users = self.service.get_active_users()
        self.assertIn(self.user1, users)
        self.assertIn(self.staff, users)
        self.assertNotIn(self.user2, users)

    def test_get_staff_users(self):
        users = self.service.get_staff_users()
        self.assertEqual(users, [self.staff])

    def test_create_and_update_user(self):
        user = self.service.create(username='new', email='new@example.com', password='pass')
        self.assertIsNotNone(user.id)
        updated = self.service.update(user, first_name='First')
        self.assertEqual(updated.first_name, 'First')
