from marshmallow import Schema, fields, post_load
from marshmallow.validate import Range

from fullask_rest_framework.vo.pagination import PaginationRequest, PaginationResponse


class PaginationRequestSchema(Schema):
    page = fields.Integer(
        validate=Range(min=1),
        metadata={"description": "The page number you want to look up."},
    )
    per_page = fields.Integer(
        validate=Range(min=1),
        metadata={"description": "The number of items on a page."},
    )

    @post_load
    def to_entity(self, data, **kwargs) -> PaginationRequest:
        return PaginationRequest(**data)


class PaginationResponseSchema(Schema):
    count = fields.Integer(metadata={"description": "Total number of items"})
    next_page = fields.Integer(metadata={"description": "Next page number"})
    previous_page = fields.Integer(metadata={"description": "Previous page number"})

    @post_load
    def to_entity(self, data, **kwargs) -> PaginationResponse:
        return PaginationResponse(**data)
