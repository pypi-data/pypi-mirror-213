from abc import ABC, abstractmethod
from typing import Generic, List, Optional

from fullask_rest_framework.repositories.base import BaseRepository, T
from fullask_rest_framework.vo.filtering import FilteringRequest
from fullask_rest_framework.vo.pagination import PaginationRequest, PaginationResponse
from fullask_rest_framework.vo.sorting import SortingRequest


class CRUDRepositoryABC(BaseRepository, ABC, Generic[T]):
    """The Base CRUD Repository class."""

    @abstractmethod
    def save(self, entity: T) -> T:
        """
        Save the given entity.

        :param entity: Entity to save.
        :return: saved Entity
        """
        pass

    @abstractmethod
    def save_all(self, entities: List[T]) -> List[T]:
        """
        Save all given entities.

        :param entities: Entities to save.
        :return: saved Entities.
        """
        pass

    @abstractmethod
    def read_by_id(self, id: int) -> Optional[T]:
        """
        Read the entity with given id.

        :return: if entity is found with given id, return it, else return None
        """
        pass

    @abstractmethod
    def is_exists_by_id(self, id) -> bool:
        """
        Check if entity with given id exists.

        :return: if entity is found with given id, return True, else return False
        """
        pass

    @abstractmethod
    def read_all(
        self,
        sorting_request: SortingRequest,
        filtering_request: FilteringRequest,
    ) -> List[Optional[T]]:
        """
        Read all entities.
        if no entities are found, return empty list.
        """
        pass

    @abstractmethod
    def read_all_with_pagination(
        self,
        pagination_request: PaginationRequest,
        sorting_request: SortingRequest,
        filtering_request: FilteringRequest,
    ) -> PaginationResponse[T]:
        """
        Read all entities with pagination.
        if no entities are found, return empty list.
        """
        pass

    @abstractmethod
    def read_all_by_ids(self, ids: List[int]) -> List[Optional[T]]:
        """
        Read all entities with given ids.

        :return: list of all entities, with given ids.
        """
        pass

    @abstractmethod
    def count(self) -> int:
        """Count all entities."""
        pass

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        """Delete the entity with given id."""

        pass

    @abstractmethod
    def delete(self, entity) -> None:
        """Delete the given entity."""
        pass

    @abstractmethod
    def delete_all_by_ids(self, ids: List[int]) -> None:
        """Delete all entities with given ids."""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Delete all entities, managed by this repository."""
        pass
