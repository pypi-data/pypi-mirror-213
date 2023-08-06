from uuid import uuid4

from fullask_rest_framework.factory.extensions import db


class BaseMixin:
    """
    The parent mixin of all mixins. Prevents mixins from being used as classes themselves.
    """

    def __init__(self, *args, **kwargs) -> None:
        if type(self) is self.__class__:
            raise TypeError(
                f"You can only use {self.__class__.__name__} for implementing Mixin."
            )
        super().__init__(*args, **kwargs)


class TimeStampedMixin(BaseMixin):
    """Mixin for auto-saving creation and modification dates"""

    created_at = db.Column(
        db.DateTime, default=db.func.now(timezone=True), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False,
    )


class UUIDMixin(BaseMixin):
    """A mixin that adds a UUID field"""

    uuid = db.Column(
        db.String(36), unique=True, nullable=False, default=lambda: str(uuid4())
    )
