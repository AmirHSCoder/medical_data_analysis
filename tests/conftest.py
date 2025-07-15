import pytest
from django.contrib.auth import get_user_model
from django.db import models
from typing import Generator, Any

User = get_user_model()

# Model Fixtures
class TestModel(models.Model):
    """A test model for repository testing"""
    __test__ = False  # prevent pytest from collecting this class as tests
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'test_app'

@pytest.fixture
def test_model() -> type[TestModel]:
    """Fixture that provides the test model class"""
    return TestModel

# User Fixtures
@pytest.fixture
def test_user() -> User:
    """Fixture that provides a basic test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_staff_user() -> User:
    """Fixture that provides a test staff user"""
    return User.objects.create_user(
        username='staffuser',
        email='staff@example.com',
        password='testpass123',
        is_staff=True
    )

@pytest.fixture
def test_inactive_user() -> User:
    """Fixture that provides a test inactive user"""
    return User.objects.create_user(
        username='inactiveuser',
        email='inactive@example.com',
        password='testpass123',
        is_active=False
    )

# Test Data Fixtures
@pytest.fixture
def test_model_data() -> dict[str, Any]:
    """Fixture that provides test data for TestModel"""
    return {
        'name': 'Test Item',
        'description': 'Test Description',
        'is_active': True
    }

@pytest.fixture
def test_user_data() -> dict[str, Any]:
    """Fixture that provides test data for User model"""
    return {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'testpass123',
        'first_name': 'New',
        'last_name': 'User'
    }

# Database Fixtures
@pytest.fixture
def enable_db_access_for_all_tests(db):
    """Provide database access when explicitly requested."""
    pass

# Custom Markers
def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line(
        "markers",
        "repository: mark test as a repository test"
    )
    config.addinivalue_line(
        "markers",
        "user_repository: mark test as a user repository test"
    ) 