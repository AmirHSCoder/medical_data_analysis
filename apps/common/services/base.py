from abc import ABC
from typing import Generic, TypeVar
from apps.common.repositories.base import BaseRepository

T = TypeVar('T')


class BaseService(Generic[T], ABC):
    """Base service providing CRUD operations via a repository."""

    repository_class: type[BaseRepository]

    def __init__(self, repository: BaseRepository | None = None) -> None:
        self.repository = repository or self.repository_class()

    def get_by_id(self, pk: int) -> T | None:
        return self.repository.get_by_id(pk)

    def get_all(self):
        return self.repository.get_all()

    def create(self, **kwargs) -> T:
        return self.repository.create(**kwargs)

    def update(self, instance: T, **kwargs) -> T:
        return self.repository.update(instance, **kwargs)

    def delete(self, instance: T) -> None:
        self.repository.delete(instance)

    def filter(self, **filters):
        return self.repository.filter(**filters)
