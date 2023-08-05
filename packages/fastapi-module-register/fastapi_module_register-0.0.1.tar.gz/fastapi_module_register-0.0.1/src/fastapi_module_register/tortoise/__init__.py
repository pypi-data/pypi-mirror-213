from typing import Any, Dict, List, Union

from fastapi import FastAPI

from .tortoise_register import TortoiseRegister
from ..logger import logger
from ..schema import ModuleConfig
from ..utils import get_module_config


def router_register(
    app: FastAPI,
    module_config: Union[List[str], List[ModuleConfig], List[Dict[str, Any]]]
) -> None:
    """_summary_

    Args:
        app (FastAPI): _description_
        module_config (Union[List[str], List[ModuleConfig], List[Dict[str, Any]]]): _description_. Defaults to None.
    """
    if not module_config:
        logger.info("No module register.")
        return

    if not isinstance(app, FastAPI):
        raise RuntimeError("Please given fastapi object.")
    
    module_config = get_module_config(module_config)
    @app.on_event("startup")
    async def init_router() -> None:  # pylint: disable=W0612
        modules = TortoiseRegister.init(app, module_config)
        logger.info("Register tortoise router started, %s", modules)
