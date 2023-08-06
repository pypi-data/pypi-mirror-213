from flask_marshmallow import Schema  # type: ignore[import]
from marshmallow import post_load

from fullask_rest_framework.schemas import fields
from fullask_rest_framework.vo.sorting import SortingRequest


class SortingRequestSchema(Schema):
    sort_by = fields.Sorting(
        metadata={
            "description": "The sort condition. It must conform to the format `fieldname:sortcondition (asc or desc)`."
        }
    )

    @post_load
    def to_entity(self, data, **kwargs) -> SortingRequest:
        data = data.get("sort_by")
        if data:
            return SortingRequest(*data)
        return SortingRequest()
