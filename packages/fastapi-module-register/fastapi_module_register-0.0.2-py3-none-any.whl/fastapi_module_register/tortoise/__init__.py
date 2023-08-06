from typing import Any, Dict, List, Union

from fastapi import FastAPI

from fastapi_module_register.logger import logger
from fastapi_module_register.schema import ModuleConfig
from fastapi_module_register.tortoise.tortoise_register import TortoiseRegister
from fastapi_module_register.utils import get_module_configs


def router_register(
    app: FastAPI,
    module_configs: Union[List[str], List[ModuleConfig], List[Dict[str, Any]]]
) -> None:
    """_summary_

    Args:
        app (FastAPI): _description_
        module_configs (Union[List[str], List[ModuleConfig], List[Dict[str, Any]]]): _description_. Defaults to None.
    """
    if not module_configs:
        logger.info("No module register.")
        return

    if not isinstance(app, FastAPI):
        raise RuntimeError("Please given fastapi object.")

    module_configs = get_module_configs(module_configs)
    @app.on_event("startup")
    async def init_router() -> None:  # pylint: disable=W0612
        modules = TortoiseRegister.init(app, module_configs)
        logger.info("Register tortoise router started, %s", modules)
