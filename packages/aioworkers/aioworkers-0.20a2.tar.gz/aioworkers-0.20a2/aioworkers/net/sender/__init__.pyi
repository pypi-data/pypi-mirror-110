import abc
from abc import abstractmethod
from aioworkers.core.base import AbstractEntity as AbstractEntity
from typing import Any

class AbstractSender(AbstractEntity, metaclass=abc.ABCMeta):
    @abstractmethod
    async def send_message(self, msg: Any) -> Any: ...
    async def send(self, *args: Any, **kwargs: Any) -> None: ...
