import glob
import logging
import os
from pathlib import Path

import yaml
from dynaconf import Dynaconf

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = Path(__file__).parent

logging.info(f"Base directory: {BASE_DIR}")


def get_config_files(file_pattern):
    return glob.glob(str(BASE_DIR / file_pattern))


config_patterns = [
    "config/base.yaml",
    ".secrets.yaml",
    "config/device_groups/*.yaml",
    "config/objects/*.yaml",
    "config/network/*.yaml",
    "config/policy/*.yaml",
    "config/device/*.yaml",
]

config_files = []
for pattern in config_patterns:
    config_files.extend(get_config_files(pattern))

logging.info("Config files to be loaded:")
for file in config_files:
    logging.info(f"  {file}")


def deep_merge(d1, d2):
    """
    Merge two dictionaries deeply.
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


# Load and merge YAML files manually
merged_config = {}
for file in config_files:
    try:
        with open(file, 'r') as f:
            config = yaml.safe_load(f)
            if config:
                merged_config = deep_merge(merged_config, config)
            else:
                logging.info(f"Skipping empty or invalid YAML file: {file}")
    except yaml.YAMLError:
        logging.info(f"Skipping invalid YAML file: {file}")
    except Exception as e:
        logging.info(f"Error processing file {file}: {str(e)}")

# Create Dynaconf settings object
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    environments=True,
    load_dotenv=True,
    merge_enabled=True,
)

# Add merged config to settings
settings.update(merged_config)

logging.info("\nLoaded settings:")
logging.info(settings.as_dict())

# Access nested settings
if 'panos_config' in settings:
    logging.info("\nPAN-OS Config:")
    logging.info(settings.panos_config.to_dict())

# Check for DYNACONF environment variables
logging.info("\nDYNACONF environment variables:")
for key, value in os.environ.items():
    if key.startswith("DYNACONF_"):
        logging.info(f"{key}: {value}")
