from typing import Generic, Type, TypeVar

from fullask_rest_framework.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    """
    The Base Repository class of all Repositories.
    """

    def __init__(self, entity: Type[T]):
        """
        :param entity: The types of entities you want to cover in this repository.
        """
        self.entity = entity
