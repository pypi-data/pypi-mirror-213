from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Union

from pydantic import StrictFloat, StrictInt, StrictStr
from pydantic.validators import strict_str_validator

from clipped.config.constants import PARAM_REGEX

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


class RefField(StrictStr):
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield strict_str_validator
        yield cls.validate

    @classmethod
    def validate(cls, value, **kwargs):
        if not isinstance(value, str):
            return value

        field = kwargs.get("field")
        param = PARAM_REGEX.search(value)
        if not param:  # TODO: Fix error message
            raise ValueError(
                f"Field `{field.name}` value must be equal to `{field.default}`, received `{value}` instead."
            )
        return value


BoolOrRef = Union[bool, RefField]
IntOrRef = Union[StrictInt, RefField]
StrictFloatOrRef = Union[StrictFloat, RefField]
FloatOrRef = Union[float, RefField]
DatetimeOrRef = Union[datetime, RefField]
TimeDeltaOrRef = Union[timedelta, RefField]
