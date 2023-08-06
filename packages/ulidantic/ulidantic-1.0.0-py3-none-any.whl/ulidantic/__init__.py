from typing import Union
from pydantic.json import ENCODERS_BY_TYPE
import ulid
import re

ULID_ACCEPT_TYPES = Union[str, bytes, ulid.ULID]


class ULIDantic(ulid.ULID):
    """
    Object Id field. Compatible with Pydantic.
    """

    valid_regex = "^[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}$"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            # TODO: #26 send PR to upstream
            if not re.match(cls.valid_regex, v):
                raise ValueError("Invalid ULID")
            return cls.from_str(v)
        elif isinstance(v, bytes):
            return cls.from_bytes(v)
        elif isinstance(v, ulid.ULID):
            return cls.from_bytes(v.bytes)
        else:
            raise TypeError("str, bytes, ULID required")

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            # simplified regex here for brevity, see the wikipedia link above
            pattern="^[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}$",
            type="string",
            examples=["01BX5ZZKBKACTAV9WEVGEMMVRZ", "01BX5ZZKBKZZZZZZZZZZZZZZZY"],
        )


ENCODERS_BY_TYPE[
    ULIDantic
] = str  # it is a workaround to force pydantic make json schema for this field
