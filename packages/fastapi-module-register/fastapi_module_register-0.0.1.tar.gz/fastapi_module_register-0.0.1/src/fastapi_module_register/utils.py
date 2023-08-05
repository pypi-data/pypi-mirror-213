from importlib import import_module
from typing import Any, Dict, List, Union
import warnings

from .constants import DEFAULT_METHODS
from .schema import RouterConfig, ModuleConfig


def get_module_config(
    module_config: Union[List[str], List[ModuleConfig], List[Dict[str, Any]]]
) -> List[ModuleConfig]:
    """_summary_

    Args:
        module_config (Union[List[str], List[ModuleConfig], List[Dict[str, Any]]]): _description_

    Returns:
        List[ModuleConfig]: _description_
    """
    configs: List[ModuleConfig] = []
    if not module_config:
        return configs
    
    for item in module_config:
        if isinstance(item, ModuleConfig):
            configs.append(item)
            continue
        if isinstance(item, str):
            temp_module_config = ModuleConfig(module_path=item)
            temp_module_config.router_config = [
                RouterConfig(method=method)
                for method in DEFAULT_METHODS
            ]
            configs.append(temp_module_config)
            continue
        if isinstance(item, Dict):
            module_config = ModuleConfig(**item)
            configs.append(module_config)
            continue
        warnings.warn(f'Unkonwn type "{item}"', RuntimeWarning, stacklevel=4)

    return configs


def import_string(dotted_path: str) -> Any:
    """import model and return cls

    Args:
        dotted_path (str): [description]

    Returns:
        any: [description]
    """

    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path} doesn't look like a module path") from err

    module: Any = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(f"Module '{module_path}' does not define a '{class_name}' attribute/class") from err


def api_path_handler(api_path: str) -> str:
    """add / for api path

    Args:
        api_path (str): _description_

    Returns:
        str: _description_
    """
    api_path = api_path if api_path.startswith("/") else f"/{api_path}"
    api_path = api_path if api_path.endswith("/") else f"{api_path}/"
    return api_path
