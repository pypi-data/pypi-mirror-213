from importlib import import_module
from typing import Any, Dict, List, Union
import warnings

from fastapi_module_register.schema import ModuleConfig


def get_module_configs(
    module_configs: Union[List[str], List[ModuleConfig], List[Dict[str, Any]]]
) -> List[ModuleConfig]:
    """_summary_

    Args:
        module_configs (Union[List[str], List[ModuleConfig], List[Dict[str, Any]]]): _description_

    Returns:
        List[ModuleConfig]: _description_
    """
    modules: List[ModuleConfig] = []
    if not module_configs:
        return modules
    
    for module_config in module_configs:
        if isinstance(module_config, ModuleConfig):
            modules.append(module_config)
            continue
        if isinstance(module_config, str):
            temp_module_config = ModuleConfig(module_path=module_config)
            temp_module_config.add_default_router_configs()
            modules.append(temp_module_config)
            continue
        if isinstance(module_config, Dict):
            temp_module_config = ModuleConfig(**module_config)
            modules.append(temp_module_config)
            continue
        warnings.warn(f'Unkonwn type "{module_config}"', RuntimeWarning, stacklevel=4)
    return modules


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
