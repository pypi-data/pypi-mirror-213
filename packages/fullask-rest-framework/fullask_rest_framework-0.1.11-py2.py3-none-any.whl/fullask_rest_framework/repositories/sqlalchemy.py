from functools import wraps
from typing import Generic, List, Optional, Type

from flask_marshmallow.sqla import SQLAlchemyAutoSchema  # type: ignore[import]
from flask_sqlalchemy.query import Query
from sqlalchemy import inspect, select

from fullask_rest_framework.repositories.base import T
from fullask_rest_framework.repositories.crud import CRUDRepositoryABC
from fullask_rest_framework.vo.filtering import FilteringRequest
from fullask_rest_framework.vo.pagination import PaginationRequest, PaginationResponse
from fullask_rest_framework.vo.sorting import SortingRequest


class SQLAlchemyFullRepository(CRUDRepositoryABC, Generic[T]):
    """
    The implementation of CRUDRepositoryABC, with SQLAlchemy.
    this implementation has dependency with flask-sqlalchemy's SQLAlchemy object.
    """

    ENTITY_CLS: Type[T]

    def __init__(self, db):
        self.db = db
        self.sqlalchemy_model = self._configure_entity()

    def save(self, entity: T) -> T:
        if hasattr(entity, "id") and entity.id:
            model_instance = self.db.session.get(self.sqlalchemy_model, entity.id)
            if model_instance:
                self._update_model_with_entity(model_instance, entity)
        else:
            model_instance = self._entity_to_sqlalchemy_model(entity)
            self.db.session.add(model_instance)
        self.db.session.commit()
        self.db.session.refresh(model_instance)
        return self._sqlalchemy_model_to_entity(model_instance)

    def save_all(self, entities: List[T]) -> List[T]:
        saved_entities = []
        for entity in entities:
            saved_entity = self.save(entity)
            saved_entities.append(saved_entity)
        return saved_entities

    def read_by_id(self, id: int) -> Optional[T]:
        query_result = self.db.session.get(self.sqlalchemy_model, id)
        if query_result:
            return self._sqlalchemy_model_to_entity(query_result)
        return None

    def is_exists_by_id(self, id) -> bool:
        if id is None:
            raise ValueError("id cannot be None.")
        return bool(self.db.session.get(self.sqlalchemy_model, id))

    def read_all(
        self,
        sorting_request: Optional[SortingRequest] = None,
        filtering_request: Optional[FilteringRequest] = None,
    ) -> List[Optional[T]]:
        query = self._get_base_query()
        if filtering_request:
            query = self._filtering(query=query, filtering_request=filtering_request)
        if sorting_request:
            query = self._sorting(query=query, sorting_request=sorting_request)
        else:
            # if no pagination request, return all results without pagination.
            return [
                self._sqlalchemy_model_to_entity(query_result)
                for query_result in self.db.session.execute(
                    select(self.sqlalchemy_model)
                )
                .scalars()
                .all()
            ]

    def read_all_with_pagination(
        self,
        pagination_request: PaginationRequest,
        sorting_request: Optional[SortingRequest] = None,
        filtering_request: Optional[FilteringRequest] = None,
    ) -> PaginationResponse[T]:
        query = self._get_base_query()
        if filtering_request:
            query = self._filtering(query=query, filtering_request=filtering_request)
        if sorting_request:
            query = self._sorting(query=query, sorting_request=sorting_request)
        query = query.paginate(
            page=pagination_request.page,
            per_page=pagination_request.per_page,
            error_out=False,
        )
        return PaginationResponse(
            count=query.total,
            next_page=query.next_num,
            previous_page=query.prev_num,
            results=[self._sqlalchemy_model_to_entity(item) for item in query.items],
        )

    def read_all_by_ids(self, ids: List[int]) -> List[Optional[T]]:
        return [self.read_by_id(_id) for _id in ids]

    def count(self) -> int:
        return self.db.session.query(self.sqlalchemy_model).count()

    def delete_by_id(self, id: int) -> None:
        model_instance = self.db.session.get(self.sqlalchemy_model, id)
        if model_instance:
            self.db.session.delete(self.db.session.get(self.sqlalchemy_model, id))
            self.db.session.commit()
        else:
            raise ValueError(f"{self.sqlalchemy_model} with id {id} not found.")

    def delete(self, entity) -> None:
        model_instance = self.db.session.get(self.sqlalchemy_model, entity.id)
        if not model_instance:
            raise ValueError(
                f"{self.sqlalchemy_model} with entity {entity} not found.\n"
                f"make sure the entity instance is stored in database."
            )
        self.db.session.delete(model_instance)
        self.db.session.commit()

    def delete_all_by_ids(self, ids: List[int]) -> None:
        self.db.session.query(self.sqlalchemy_model).filter(
            self.sqlalchemy_model.id.in_(ids)
        ).delete()

    def delete_all(self) -> None:
        self.sqlalchemy_model.query.delete()

    def _get_base_query(self) -> Query:
        return self.db.session.query(self.sqlalchemy_model)

    def _filtering(self, query: Query, filtering_request: FilteringRequest) -> Query:
        """
        filter the query with filtering_object.
        this is implementation of `or` condition.
        """
        for field, word in vars(filtering_request).items():
            query = query.filter(
                getattr(self.sqlalchemy_model, field).ilike(f"%{word}%")
            )
        return query

    def _sorting(self, query: Query, sorting_request: SortingRequest) -> Query:
        for field, direction in vars(sorting_request).items():
            if direction == "asc":
                query = query.order_by(getattr(self.sqlalchemy_model, field).asc())
            elif direction == "desc":
                query = query.order_by(getattr(self.sqlalchemy_model, field).desc())
        return query

    def _sqlalchemy_model_to_entity(self, sqlalchemy_instance) -> T:
        assert isinstance(
            sqlalchemy_instance, self.sqlalchemy_model
        ), f"{sqlalchemy_instance} is not {self.sqlalchemy_model}"
        sqlalchemy_model_pk_names = [
            pk.name for pk in inspect(self.sqlalchemy_model).primary_key
        ]
        if len(sqlalchemy_model_pk_names) == 1:
            instance_dict = sqlalchemy_instance.__dict__
            instance_dict.pop("_sa_instance_state")
            return self.ENTITY_CLS(**instance_dict)
        else:
            raise ValueError("multi-pk case is not supported in current version.")

    def _entity_to_sqlalchemy_model(self, entity):
        assert isinstance(
            entity, self.ENTITY_CLS
        ), f"{entity} is not instance of {self.ENTITY_CLS}"
        return self.sqlalchemy_model(**self._get_sqlalchemy_schema().dump(entity))

    def _get_sqlalchemy_schema(self) -> SQLAlchemyAutoSchema:
        class SQLAlchemyModelSchema(SQLAlchemyAutoSchema):
            class Meta:
                model = self.sqlalchemy_model

        return SQLAlchemyModelSchema()

    @staticmethod
    def _update_model_with_entity(model_instance, entity):
        # Iterate over the fields of the entity object
        for field_name, field_value in entity.__dict__.items():
            if field_name != "id":
                setattr(model_instance, field_name, field_value)

    def _configure_entity(self) -> Type[T]:
        """
        This method will find if there is a SQLAlchemy model class defined based on the entity class name.

        The rules to look for are as follows:
        {entity class name - "Entity"} + "Model"

        For example, if the entity is named "CarEntity", the method will try to find the "CarModel" class.
        """
        models = {
            mapper.class_.__name__: mapper.class_
            for mapper in self.db.Model.registry.mappers
        }
        for model_name, mapper_class in models.items():
            if model_name == self.ENTITY_CLS.__name__.replace("Entity", "") + "Model":
                return mapper_class


def read_by_fields(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        field_name = func.__name__[len("read_by_") :]
        if field_name in kwargs:
            field_value = kwargs[field_name]
        else:
            if len(args) < 1:
                raise ValueError(f"{field_name} argument is missing")
            field_value = args[0]
        query_result = self.sqlalchemy_model.query.filter_by(
            **{field_name: field_value}
        ).first()
        if query_result:
            return self._sqlalchemy_model_to_entity(query_result)
        return None

    return wrapper
