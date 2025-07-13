from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.common.repositories.user_repository import UserRepository
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

User = get_user_model()

class TestUserRepository(TestCase):
    def setUp(self):
        self.repository = UserRepository()
        # Create test users with different states
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User1',
            is_active=True
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User2',
            is_active=False
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='testpass123',
            first_name='Staff',
            last_name='User',
            is_staff=True,
            is_active=True
        )

    def test_get_by_username_existing(self):
        """Test getting a user by existing username"""
        user = self.repository.get_by_username('testuser1')
        self.assertEqual(user, self.user1)
        self.assertEqual(user.email, 'test1@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User1')

    def test_get_by_username_nonexistent(self):
        """Test getting a user by non-existent username"""
        user = self.repository.get_by_username('nonexistent')
        self.assertIsNone(user)

    def test_get_by_id_existing(self):
        """Test getting a user by ID"""
        user = self.repository.get_by_id(self.user1.id)
        self.assertEqual(user, self.user1)
        self.assertEqual(user.username, 'testuser1')

    def test_get_by_id_nonexistent(self):
        """Test getting a non-existent user by ID"""
        user = self.repository.get_by_id(999)
        self.assertIsNone(user)

    def test_get_all(self):
        """Test getting all users"""
        all_users = self.repository.get_all()
        self.assertEqual(len(all_users), 3)
        self.assertTrue(all(isinstance(user, User) for user in all_users))

    def test_create(self):
        """Test creating a new user"""
        user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'testpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        new_user = self.repository.create(**user_data)
        self.assertIsNotNone(new_user.id)
        self.assertEqual(new_user.username, 'newuser')
        self.assertEqual(new_user.email, 'new@example.com')

    def test_update(self):
        """Test updating a user"""
        update_data = {
            'username': 'updated_username',
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        updated_user = self.repository.update(self.user1, **update_data)
        self.assertEqual(updated_user.username, 'updated_username')
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')

    def test_delete(self):
        """Test deleting a user"""
        user_id = self.user1.id
        self.repository.delete(self.user1)
        self.assertFalse(User.objects.filter(id=user_id).exists())

    def test_create_user_with_duplicate_username(self):
        """Test creating a user with duplicate username"""
        with self.assertRaises(IntegrityError):
            self.repository.create(
                username='testuser1',  # Same as user1
                email='different@example.com',
                password='testpass123'
            )

    def test_get_active_users(self):
        """Test getting all active users"""
        active_users = self.repository.get_active_users()
        self.assertEqual(len(active_users), 2)  # user1 and staff_user
        self.assertIn(self.user1, active_users)
        self.assertIn(self.staff_user, active_users)
        self.assertNotIn(self.user2, active_users)
        
        # Verify user details
        for user in active_users:
            self.assertTrue(user.is_active)

    def test_get_staff_users(self):
        """Test getting all staff users"""
        staff_users = self.repository.get_staff_users()
        self.assertEqual(len(staff_users), 1)
        self.assertEqual(staff_users[0], self.staff_user)
        self.assertTrue(staff_users[0].is_staff)

    def test_filter_users_by_name(self):
        """Test filtering users by name"""
        # Test filtering by first name
        users = self.repository.filter(first_name='Test')
        self.assertEqual(len(users), 2)
        self.assertTrue(all(user.first_name == 'Test' for user in users))

        # Test filtering by last name
        users = self.repository.filter(last_name='User1')
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], self.user1)

    def test_filter_users_by_active_status(self):
        """Test filtering users by active status"""
        active_users = self.repository.filter(is_active=True)
        self.assertEqual(len(active_users), 2)
        self.assertTrue(all(user.is_active for user in active_users))

        inactive_users = self.repository.filter(is_active=False)
        self.assertEqual(len(inactive_users), 1)
        self.assertFalse(inactive_users[0].is_active) 