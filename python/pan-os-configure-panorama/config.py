import glob
from pathlib import Path
from typing import List, Dict, Any, Optional

import yaml
from dynaconf import Dynaconf
from yaml.error import YAMLError

from utils import logger

BASE_DIR: Path = Path(__file__).parent


def get_config_files(file_pattern: str) -> List[str]:
    """
        Retrieve a list of configuration files matching a given pattern.

        This function uses glob to find files in the BASE_DIR directory that match the specified pattern.

        Attributes:
            file_pattern (str): The pattern to match configuration files.

        Return:
            List[str]: A list of file paths matching the given pattern.
    """

    return glob.glob(str(BASE_DIR / file_pattern))


config_patterns: List[str] = [
    "config/base.yaml",
    ".secrets.yaml",
    "config/device_groups/*.yaml",
    "config/objects/*.yaml",
    "config/network/*.yaml",
    "config/policy/*.yaml",
    "config/device/*.yaml",
]

config_files: List[str] = []
for pattern in config_patterns:
    config_files.extend(get_config_files(pattern))


def deep_merge(
    d1: Dict[str, Any],
    d2: Dict[str, Any],
) -> Dict[str, Any]:
    """
        Deeply merge two dictionaries.

        Recursively combines nested dictionaries and lists from d2 into d1.
        If a key exists in both dictionaries, d2's value takes precedence for non-dict values.

        Args:
            d1 (Dict[str, Any]): The base dictionary to merge into.
            d2 (Dict[str, Any]): The dictionary to merge from.

        Return:
            Dict[str, Any]: The merged dictionary.
    """
    if not isinstance(d1, dict):
        return d2
    if not isinstance(d2, dict):
        return d1
    for config_key, config_value in d2.items():
        if isinstance(config_value, dict):
            d1[config_key] = deep_merge(d1.get(config_key, {}), config_value)
        elif isinstance(config_value, list):
            d1[config_key] = d1.get(config_key, []) + config_value
        else:
            d1[config_key] = config_value
    return d1


def load_yaml_file(file_path: str) -> Optional[Dict[str, Any]]:
    """
        Load and parse a YAML file, returning its contents as a dictionary.

        Attempts to open and parse the specified YAML file, handling potential errors
        such as parsing issues, file I/O problems, or unexpected exceptions.

        Attributes:
            file_path (str): The path to the YAML file to be loaded.

        Error:
            YAMLError: If there's an error parsing the YAML file.
            IOError: If there's an error reading the file.
            Exception: For any unexpected errors during file loading.

        Return:
            Optional[Dict[str, Any]]: The parsed YAML content as a dictionary, or None if an error occurs.
    """

    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except YAMLError as e:
        logger.error(f"Error parsing YAML file {file_path}: {e}")
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading file {file_path}: {e}")
    return None


# Load and merge YAML files manually
merged_config: Dict[str, Any] = {}
for file in config_files:
    config = load_yaml_file(file)
    if config:
        merged_config = deep_merge(merged_config, config)
    else:
        logger.warning(f"Skipping file {file} due to loading error")

# Create Dynaconf settings object
try:
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        environments=True,
        load_dotenv=True,
        merge_enabled=True,
    )

    # Add merged config to settings
    settings.update(merged_config)
except Exception as e:
    logger.critical(f"Failed to initialize Dynaconf settings: {e}")
    raise
