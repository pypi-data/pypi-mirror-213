import re
import typing

from marshmallow import fields, utils


class Sorting(fields.Field):
    """
    Overrides the field to make it easier
    to parse `<operator>fieldname` in the URL.
    """

    default_error_messages = {"invalid": "Not a valid Sorting."}

    def _deserialize(
        self,
        value: typing.Any,
        attr: str | None,
        data: typing.Mapping[str, typing.Any] | None,
        **kwargs,
    ):
        if not isinstance(value, (str, bytes)):
            raise self.make_error("invalid")
        try:
            value = utils.ensure_text_type(value)
            # validate the value, make sure it's a valid sort information.
            pattern = r"^[a-zA-Z_]+:(asc|desc)(,[a-zA-Z_]+:(asc|desc))*$"
            if not re.match(pattern, value):
                raise self.make_error("invalid")
            # change the format, like {fieldname:asc,fieldname2:desc}
            sorting_infos = value.split(",")
            return [
                {sorting_info.split(":")[0]: sorting_info.split(":")[1]}
                for sorting_info in sorting_infos
            ]

        except UnicodeDecodeError as error:
            raise self.make_error("invalid_utf8") from error
