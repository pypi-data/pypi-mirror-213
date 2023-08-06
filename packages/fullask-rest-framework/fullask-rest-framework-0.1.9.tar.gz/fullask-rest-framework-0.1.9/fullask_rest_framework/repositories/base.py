from typing import Generic, TypeVar

from fullask_rest_framework.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    """
    The Base Repository class of all Repositories.
    """
