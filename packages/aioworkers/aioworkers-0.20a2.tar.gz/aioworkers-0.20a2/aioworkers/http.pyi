import abc
from typing import Any

class _URL(str, abc.ABC):
    def __init__(self, *args: Any) -> None: ...
    @property
    def path(self): ...
    def __truediv__(self, other: Any): ...

URL: Any
