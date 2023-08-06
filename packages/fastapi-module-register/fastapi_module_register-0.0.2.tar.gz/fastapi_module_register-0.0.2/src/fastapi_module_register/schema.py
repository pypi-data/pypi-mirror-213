from datetime import datetime
from typing import Any, Dict, List, Generic, Optional, TypeVar

import ujson as json
from pydantic import BaseModel, Extra, Field
from pydantic.generics import GenericModel


_T = TypeVar("_T")


class RouterConfig(BaseModel):
    api_path: str = Field(None, description="The api router path")
    method: str = Field('get', description="The api request method")
    parameters: Dict = {}

    class Config:
        schema_extra = {
            "example": {
                "api_path": "/api/example",
                "enable_methods": ["get"],
                "parameters": {
                    "tags": ["example"]
                }
            }
        }


class ModuleConfig(BaseModel):
    name: str = Field(None, description="The module name")
    module_path: str = Field(..., description="The module path")
    module: Any = None
    router_config: List[RouterConfig] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "example",
                "module_path": ["models.example"],
                "router_config": [
                    {
                        "api_path": "/api/example",
                        "method": "get",
                        "parameters": {
                            "tags": ["example"]
                        }
                    }
                ]
            }
        }

    def get_router_config(self, method: str, api_path: str, module_name: str) -> RouterConfig:
        """_summary_

        Args:
            method (str): The router method
            api_path (str): The router path
            module_name (str): The module name

        Returns:
            RouterConfig: _description_
        """
        router_config = RouterConfig(
            api_path=api_path,
            method=method,
            parameters={
                "tags": [module_name],
                "summary": f"{method.title()} {module_name}",
                "description": f"{method.title()} {module_name}"
            }
        )
        return router_config

    def add_default_router_configs(self) -> None:
        """add default router configs
        """
        if not self.module_path:
            return

        module_name = self.module_path.rsplit(".")[-1]
        default_apis = {
            "get": f"/{module_name}s/",
            "post": f"/{module_name}s/",
            "put": f"/{module_name}/" + "{pk}",
            "patch": f"/{module_name}s/",
            "delete": f"/{module_name}/" + "{pk}"
        }
        for method, api_path in default_apis.items():
            router_config = self.get_router_config(method, api_path, module_name) 
            self.router_config.append(router_config)

        router_config = self.get_router_config(
            "get",
            f"/{module_name}/" + "{pk}",
            module_name
        )
        self.router_config.append(router_config)

class BaseApiSchema(BaseModel):
    class Config:
        extra = Extra.allow
        json_loads = json.loads
        json_dumps = json.dumps
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
        }


class BaseApiOut(GenericModel, Generic[_T], BaseApiSchema):
    msg: str = "success"
    data: Optional[_T] = None
    code: int = 0
