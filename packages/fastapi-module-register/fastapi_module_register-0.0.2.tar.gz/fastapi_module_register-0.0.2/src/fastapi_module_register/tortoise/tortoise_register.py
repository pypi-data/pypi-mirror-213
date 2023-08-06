from typing import Any, Dict, List, Optional, Type
import warnings

from fastapi import FastAPI
from tortoise.models import Model
from tortoise.contrib.fastapi import HTTPNotFoundError

from fastapi_module_register.base_register import BaseRegister
from fastapi_module_register.exceptions import ConfigurationError
from fastapi_module_register.schema import ModuleConfig
from fastapi_module_register.tortoise.tortoise_method import TortoiseMethod
from fastapi_module_register.utils import import_string 


class TortoiseRegister(BaseRegister):

    @classmethod
    def init(cls, app: FastAPI, module_configs: List[ModuleConfig]) -> None:
        if cls._inited or not module_configs:
            return
        
        cls.load_modules(module_configs)
        routers = cls.load_routers()
        cls.add_router(app, routers)

    @classmethod
    def load_modules(cls, module_configs: List[ModuleConfig]) -> None:
        """load modules

        Args:
            app (FastAPI): _description_
            modules (Optional[List[str]]): _description_
        """
        for module_config in module_configs:
            # Loading module
            module = cls._discover_model(module_config.module_path)
            if not module:
                continue
            module_config.module = module
            if not module_config.name:
                module_config.name = module.__name__
        cls.modules = {model.name: model for model in module_configs}

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
    def load_routers(cls) -> List[Any]:
        """load routers

        Returns:
            _type_: _description_
        """
        
        routers = []
        for _, module_config in cls.modules.items():
            if not issubclass(module_config.module, Model):
                warnings.warn(f"The module is not a type model")
                continue

            tortoise_method = TortoiseMethod(module_config.module)
            for config in module_config.router_config:
                exec_fun = getattr(tortoise_method, config.method, None)
                if not exec_fun:
                    warnings.warn(f"Unsupported http method: {config.method}")
                    continue

                if config.method.lower() == "get":
                    filter_by_pk = True if '{pk}' in config.api_path else False
                    exec_fun_obj, req_schema = exec_fun(filter_by_pk)
                else:
                    exec_fun_obj, req_schema = exec_fun()
                if not callable(exec_fun_obj):
                    continue

                router = {
                    "path": config.api_path,
                    "endpoint": exec_fun_obj,
                    "methods": [config.method],
                    "response_model": req_schema,
                    "responses": {404: {"model": HTTPNotFoundError}}
                }
                router.update(config.parameters)
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
