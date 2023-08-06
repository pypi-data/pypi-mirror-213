"""Configuration utilities"""
import configparser
import contextlib
import os
from pathlib import Path
from typing import Optional

from mlsteam_model_sdk.core.exceptions import MissingConfigException


__config_path = None
__config = None
CFG_DIR = '.mlsteam-model-sdk'
CFG_FILE = 'cfg.ini'
CFG_SECTION = 'mlsteam_model_sdk'

OPTION_API_TOKEN = 'api_token'
OPTION_API_ENDPOINT = 'api_endpoint'
OPTION_DEFAULT_PUUID = 'default_puuid'
OPTION_DEFAULT_PROJECT_NAME = 'default_project_name'
OPTION_DEFAULT_MUUID = 'default_muuid'
OPTION_DEFAULT_MODEL_NAME = 'default_model_name'


def get_config_path(check: bool = False) -> Optional[Path]:
    """Gets SDK configuration file path.

    It performs configuration discovery if such a path has not been initialized. Discovery order:
    1. current working directory
    2. home directory
    3. working directory upward

    Args:
      check: whether to check configuation existence

    Returns:
      path to the configuration file, or `None` if the file is not found and check is `False`

    Raises:
      MissingConfigException: configuration is not found (when check is `True`)
    """
    if __config_path:
        return __config_path

    # current working dir
    curr_dir = Path().absolute()

    if False:
        curr_file = NotImplemented

    def _walrus_wrapper_curr_file_5017c7268cf34d2f9d237a0b14110546(expr):
        """Wrapper function for assignment expression."""
        nonlocal curr_file
        curr_file = expr
        return curr_file

    if (_walrus_wrapper_curr_file_5017c7268cf34d2f9d237a0b14110546(curr_dir / CFG_DIR / CFG_FILE)).is_file():
        return curr_file

    # home dir
    with contextlib.suppress(RuntimeError):
        if False:
            curr_file = NotImplemented

        def _walrus_wrapper_curr_file_85436f4d11924a7c8ad8a2d3f9f8073e(expr):
            """Wrapper function for assignment expression."""
            nonlocal curr_file
            curr_file = expr
            return curr_file

        if (_walrus_wrapper_curr_file_85436f4d11924a7c8ad8a2d3f9f8073e(Path.home() / CFG_DIR / CFG_FILE)).is_file():
            return curr_file

    # working dir upward
    for _dir in curr_dir.parents:
        if False:
            curr_file = NotImplemented

        def _walrus_wrapper_curr_file_0b43ea92554644b68f2970266f91b534(expr):
            """Wrapper function for assignment expression."""
            nonlocal curr_file
            curr_file = expr
            return curr_file

        if (_walrus_wrapper_curr_file_0b43ea92554644b68f2970266f91b534(_dir / CFG_DIR / CFG_FILE)).is_file():
            return curr_file

    if check:
        raise MissingConfigException()

    return None


def init_config(path=None, check: bool = False):
    """Initializes SDK configuration file path.

    This function is only effective at first time. It is NOP in subsequent calls.

    NOTE: Some SDK functions initialize SDK configuration implicitly when it has not been done.
    To use a custom configuration path, it is adviced to call this function before any other SDK call.

    Args:
      path: SDK configuration file path to set. When it is not given, configuration discovery is performed.
      check: raises an exception when configuration discovery fails

    Raises:
      MissingConfigException: configuration discovery fails (when check is `True`)
    """
    global __config_path, __config

    if not __config:
        __config = configparser.ConfigParser(allow_no_value=True)

        if not path:
            path = get_config_path(check=check)
        __config_path = path
        if path:
            __config.read(path)
        else:
            __config.read_dict({})


def get_value(option: str, section: str = None):
    """Gets configuration value.

    It initializes configuration implicitly if it has not been done.
    """
    init_config()
    try:
        if section is None:
            section = CFG_SECTION
        env_key = '_'.join([section.upper(), option.upper()])
        return os.environ[env_key]
    except KeyError:
        return __config.get(section, option, fallback=None)
