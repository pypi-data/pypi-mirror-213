from typing import Any, Dict, List

from pydantic import BaseModel, Field


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
    model: Any = None
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
