"""Main application module for configuring Palo Alto Networks tunnel interfaces."""

import argparse
import os
import sys
from typing import List

import yaml
from dotenv import load_dotenv
from utils import logger, set_log_level

from models import Config
from panos_client import PanosClient


def parse_tags(tags: List[str]) -> List[str]:
    """Parse tags into a list."""
    return tags


def load_yaml_config(file_path: str) -> Config:
    """
    Load configurations from a YAML file.

    Args:
        file_path: Path to the YAML configuration file

    Returns:
        A Config object containing templates, template stacks, and their interfaces

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
    parser = argparse.ArgumentParser(description="Configure interfaces in Palo Alto Networks Panorama")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to YAML configuration file containing interface configurations",
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

            template_names = []
            template_stack_names = []

            # Process tunnel interfaces (using Template)
            if config.tunnel_interfaces:
                for template_entry in config.tunnel_interfaces:
                    # Get or create template
                    template = client.get_or_create_template(template_entry.template)
                    if not template:
                        logger.error(
                            "Failed to get/create template: %s",
                            template_entry.template,
                        )
                        continue

                    template_names.append(template_entry.template)

                    # Create tunnel interfaces
                    for tunnel in template_entry.entries:
                        # Process the IP address - in YAML it's a list but our model can handle both
                        # The client logic will handle either format now

                        if not client.create_tunnel_interface(template, tunnel):
                            logger.error(
                                "Failed to create tunnel interface: %s.%s",
                                tunnel.name,
                                tunnel.subinterface,
                            )
                            continue

                        logger.info(
                            "Created tunnel interface: %s.%s",
                            tunnel.name,
                            tunnel.subinterface,
                        )

            # Process loopback interfaces (using TemplateStack)
            if config.loopback_interfaces:
                for template_stack_entry in config.loopback_interfaces:
                    # Get or create template stack
                    template_stack = client.get_or_create_template_stack(template_stack_entry.template_stack)
                    if not template_stack:
                        logger.error(
                            "Failed to get/create template stack: %s",
                            template_stack_entry.template_stack,
                        )
                        continue

                    template_stack_names.append(template_stack_entry.template_stack)

                    # Create loopback interfaces
                    for loopback in template_stack_entry.entries:
                        if not client.create_loopback_interface(template_stack, loopback):
                            logger.error(
                                "Failed to create loopback interface: %s",
                                loopback.name,
                            )
                            continue

                        logger.info(
                            "Created loopback interface: %s",
                            loopback.name,
                        )

            # Commit changes if any interfaces were created
            if os.getenv("PANORAMA_COMMIT", "false").lower() == "true":
                # First commit to Panorama
                if not client.commit_to_panorama():
                    logger.error("Failed to commit changes to Panorama")
                    return 1
                logger.info("Successfully committed changes to Panorama")

                # Then push changes to templates and template stacks
                if not client.commit_all(templates=template_names, template_stacks=template_stack_names):
                    logger.error("Failed to push changes to templates/template stacks")
                    return 1
                logger.info("Successfully pushed changes to templates and template stacks")

        return 0

    except Exception as e:
        logger.error("An error occurred: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
