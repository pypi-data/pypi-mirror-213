from typing import Union

from pydantic import StrictFloat, StrictInt

IntOrFloat = Union[int, float]
StrictIntOrFloat = Union[StrictInt, StrictFloat, float]
