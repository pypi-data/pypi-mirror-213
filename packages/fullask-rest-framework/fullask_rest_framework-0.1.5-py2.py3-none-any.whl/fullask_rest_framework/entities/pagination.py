from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

from fullask_rest_framework.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


@dataclass
class PaginationResponse(Generic[T]):
    count: Optional[int]
    next_page: Optional[int]
    previous_page: Optional[int]
    results: List


@dataclass
class PaginationRequest:
    page: Optional[int] = None
    per_page: Optional[int] = None
