from abc import ABC
from typing import Any, Generic, List, Optional, Type, TypeVar

from django.db import models

T = TypeVar("T", bound=models.Model)


class BaseRepository(Generic[T], ABC):
    """
    An abstract base class for a repository.
    """

    model: Type[T]

    def get_by_id(self, pk: int) -> Optional[T]:
        """
        Returns a single instance of a model by its primary key.
        """
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return None

    def get_all(self) -> List[T]:
        """
        Returns all instances of a model.
        """
        return list(self.model.objects.all())

    def create(self, **kwargs) -> T:
        """
        Creates a new instance of a model.
        """
        return self.model.objects.create(**kwargs)

    def update(self, instance: T, **kwargs) -> T:
        """
        Updates an existing model instance.
        """
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: T) -> None:
        """
        Deletes a model instance.
        """
        instance.delete()

    def filter(self, **filters: Any) -> models.QuerySet:
        """Return a queryset filtered by the supplied arguments."""
        return self.model.objects.filter(**filters)

    def exists(self, **filters: Any) -> bool:
        """Return ``True`` if a record matching the filters exists."""
        return self.model.objects.filter(**filters).exists()
