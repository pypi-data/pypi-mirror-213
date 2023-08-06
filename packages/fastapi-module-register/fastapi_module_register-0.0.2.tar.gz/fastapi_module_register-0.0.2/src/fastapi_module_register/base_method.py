from abc import abstractmethod, ABC
from typing import Any, Callable, Optional, Tuple, Union

from tortoise.models import Model


class BaseMethod(ABC):

    @abstractmethod
    def get(cls, module: Union[Model, Any], *args, **kwars) -> Optional[Tuple[Callable, Any]]:
        raise NotImplementedError

    @abstractmethod
    def post(cls, module: Union[Model, Any], *args, **kwars) -> Optional[Tuple[Callable, Any]]:
        raise NotImplementedError

    @abstractmethod
    def put(cls, module: Union[Model, Any], *args, **kwars) -> Optional[Tuple[Callable, Any]]:
        raise NotImplementedError

    @abstractmethod
    def delete(cls, module: Union[Model, Any], *args, **kwars) -> Optional[Tuple[Callable, Any]]:
        raise NotImplementedError
