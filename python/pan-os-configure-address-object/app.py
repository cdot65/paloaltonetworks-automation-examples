"""Main application module for configuring Palo Alto Networks address objects."""

import argparse
import ipaddress
import os
import sys
from typing import List

import yaml
from dotenv import load_dotenv

from models import AddressObject, Config
from panos_client import PanosClient
from utils import logger, set_log_level, validate_ip_address


def parse_tags(tags: List[str]) -> List[str]:
    """Parse tags into a list."""
    return tags


def load_yaml_config(file_path: str) -> Config:
    """
    Load address object configurations from a YAML file.

    Args:
        file_path: Path to the YAML configuration file

    Returns:
        A dictionary containing device groups and their address objects

    Raises:
        ValueError: If the YAML file is not properly formatted
        OSError: If there are file I/O issues
        yaml.YAMLError: If there are YAML parsing issues
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise ValueError("Invalid YAML format: root must be a dictionary")
            return Config.model_validate(data)
    except (yaml.YAMLError, OSError) as e:
        logger.error("Failed to load YAML config: %s", e)
        raise


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Configure address objects in Palo Alto Networks Panorama")
    parser.add_argument(
        "--config",
        type=str,
        help="Path to YAML configuration file containing address objects",
    )
    args = parser.parse_args()
    logger.info("Parsed arguments: config=%s", args.config)
    return args


def main() -> int:
    """Execute the main application logic.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    # Load environment variables
    load_dotenv()

    # Set up logging
    log_level = os.getenv("PANORAMA_LOG_LEVEL", "INFO")
    set_log_level(log_level)

    # Parse command line arguments
    args = parse_arguments()

    try:
        # Get configuration
        hostname = os.getenv("PANORAMA_HOSTNAME")
        api_key = os.getenv("PANORAMA_API_KEY")

        if not hostname or not api_key:
            logger.error("PANORAMA_HOSTNAME and PANORAMA_API_KEY must be set")
            return 1

        # Initialize PanosClient
        client = PanosClient.connect(hostname=hostname, api_key=api_key)

        if args.config:
            # Load configuration from YAML
            config = load_yaml_config(args.config)
            logger.info("Loaded configuration from %s", args.config)

            for dg_name, dg_config in config.device_groups.items():
                # Get or create device group
                device_group = client.get_or_create_device_group(str(dg_name))
                if not device_group:
                    logger.error("Failed to get/create device group: %s", dg_name)
                    continue

                # Create address objects
                for addr_obj in dg_config.address_objects:
                    if not validate_ip_address(str(addr_obj.value)):
                        logger.error("Invalid IP address or network: %s", addr_obj.value)
                        continue

                    try:
                        ip_network = ipaddress.ip_network(str(addr_obj.value))
                        address_obj = AddressObject(
                            name=addr_obj.name,
                            value=ip_network,
                            description=addr_obj.description,
                            tags=addr_obj.tags,
                        )

                        if not client.create_address_object(device_group, address_obj):
                            logger.error("Failed to create address object: %s", addr_obj.name)
                            continue

                        logger.info("Created address object: %s", addr_obj.name)
                    except ValueError as e:
                        logger.error("Invalid IP address format: %s", e)
                        continue

            # Commit changes if any address objects were created
            if not os.getenv("PANORAMA_NO_COMMIT"):
                if not client.commit_to_panorama():
                    logger.error("Failed to commit changes to Panorama")
                    return 1
                logger.info("Successfully committed changes to Panorama")

        return 0

    except Exception as e:
        logger.error("An error occurred: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
