from abc import abstractmethod, ABC
from typing import Union, Dict, List, Any

from fastapi import FastAPI

from .schema import ModuleConfig

class BaseRegister(ABC):

    modules: Dict[str, Union[ModuleConfig, Any]] = {}
    _inited: bool = False

    @classmethod
    @abstractmethod
    def init(cls, app: FastAPI, module_configs: List[ModuleConfig], *args, **kwargs) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load_modules(cls, module_dirs: List[str], *args, **kwargs) -> List[Any]:
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def load_routers(cls) -> None:
        raise NotImplementedError
