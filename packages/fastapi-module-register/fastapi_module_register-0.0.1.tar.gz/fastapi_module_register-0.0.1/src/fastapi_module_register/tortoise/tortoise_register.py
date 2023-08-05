from typing import Callable, Dict, Type, List, Optional
import warnings

from fastapi import FastAPI
from tortoise.models import Model

from ..base_register import BaseRegister
from ..exceptions import ConfigurationError
from ..schema import ModuleConfig
from ..utils import api_path_handler, import_string 


class TortoiseRegister(BaseRegister):

    @classmethod
    def init(cls, app: FastAPI, module_configs: List[ModuleConfig]) -> None:
        if cls._inited or not module_configs:
            return
        modules = cls.load_modules(module_configs)
        routers = cls.load_routers(modules)
        cls.add_router(app, routers)

    @classmethod
    def load_modules(cls, module_configs: List[ModuleConfig]) -> Dict[str, ModuleConfig]:
        """_summary_

        Args:
            app (FastAPI): _description_
            modules (Optional[List[str]]): _description_
        """
        for module_config in module_configs:
            # Loading module
            model = cls._discover_model(module_config.module_path)
            if not model:
                continue
            module_config.model = model
            if not module_config.name:
                module_config.name = model.__name__
        return {model.name: model for model in module_configs}

    @classmethod
    def _discover_model(
        cls,
        models_path: str
    ) -> Optional[Type["Model"]]:
        """_summary_

        Raises:
            ConfigurationError: _description_

        Returns:
            _type_: _description_
        """
        
        try:
            module = import_string(models_path)
        except ImportError:
            raise ConfigurationError(f'Module "{models_path}" not found')

        if issubclass(module, Model) and not module._meta.abstract:
            if not module._meta.app:
                return None
            return module

    @classmethod
    def load_routers(cls, modules: Dict[str, ModuleConfig]) -> None:
        """_summary_

        Args:
            modules (Dict[str, ModuleConfig]]): _description_

        Returns:
            _type_: _description_
        """
        routers = []
        for name, module in modules.items():
            if not issubclass(module.model, Model):
                warnings.warn(f"The module is not a type model")

            api_path = api_path_handler(module.model.__name__)
            for config in module.router_config:
                exec_fun = getattr(cls, config.method, None)
                if not exec_fun:
                    warnings.warn(f"Unsupported http method: {config.method}")
                    continue
                exec_fun_obj = exec_fun()
                if not callable(exec_fun_obj):
                    continue
                router = {
                    "path": api_path,
                    "endpoint": exec_fun_obj,
                    "methods": [config.method],
                    "tags": [name],
                }
                routers.append(router)
        return routers

    @classmethod
    def add_router(cls, app: FastAPI, routers: List[Dict]) -> None:
        """_summary_

        Args:
            app (FastAPI): _description_
            routers (List[Dict]): _description_
        """
        if not routers:
            return
        
        for router in routers:
            app.add_api_route(**router)

    @classmethod
    def get(cls) -> Callable:
        async def get_method():
            return {"1": 2}        
        return get_method

    @classmethod
    def post(cls) -> None:
        async def post_method():
            pass

    @classmethod
    def put(cls) -> None:
        async def put_method():
            pass

    @classmethod
    def patch(cls) -> None:
        async def patch_method():
            pass

    @classmethod
    def delete(cls) -> None:
        async def delete_method():
            pass
