from django.contrib.auth import get_user_model
from apps.common.repositories.user_repository import UserRepository
from .base import BaseService

User = get_user_model()


class UserService(BaseService[User]):
    """Service layer for user-related operations."""

    repository_class = UserRepository

    def get_active_users(self):
        return self.repository.get_active_users()

    def get_staff_users(self):
        return self.repository.get_staff_users()
