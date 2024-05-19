# standard library imports
import logging
import argparse
import ast
from typing import Dict, Union

# Palo Alto Networks PAN-OS imports
from panos_upgrade_assurance.check_firewall import CheckFirewall
from panos_upgrade_assurance.firewall_proxy import FirewallProxy

# third party imports
from pydantic import BaseModel

# import ipdb

# ----------------------------------------------------------------------------
# Define workflows
# ----------------------------------------------------------------------------
READINESS_CHECKS = [
    "active_support",
    "arp_entry_exist",
    "candidate_config",
    "content_version",
    "free_disk_space",
    "expired_licenses",
    "ha",
    "ip_sec_tunnel_status",
    "ntp_sync",
    "panorama",
    "planes_clock_sync",
    "session_exist",
]

STATE_SNAPSHOTS = [
    "arp_table",
    "content_version",
    "ip_sec_tunnels",
    "license",
    "nics",
    "routes",
    "session_stats",
]

REPORTS = [
    "arp_table",
    "content_version",
    "ip_sec_tunnels",
    "license",
    "nics",
    "routes",
    "session_stats",
]


# ----------------------------------------------------------------------------
# Define logging levels
# ----------------------------------------------------------------------------
LOGGING_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


# ----------------------------------------------------------------------------
# Define models
# ----------------------------------------------------------------------------
class Args(BaseModel):
    action: str
    api_key: str
    config: dict = {}
    hostname: str
    log_level: str = "debug"
    operation_type: str
    serial: str = None
    vsys: str = None


# ----------------------------------------------------------------------------
# Parse arguments
# ----------------------------------------------------------------------------
def parse_arguments() -> Args:
    """
    Parse command line arguments and returns a Namespace object with arguments as attributes.

    The --config argument should be a string that represents a Python dictionary.
    This function converts the string to a dictionary using ast.literal_eval().

    Returns:
        argparse.Namespace: Namespace object with arguments as attributes

    Raises:
        argparse.ArgumentError: If --config argument is not a valid dictionary string.
    """
    parser = argparse.ArgumentParser(description="Run operations on the Firewall.")
    parser.add_argument(
        "--action",
        dest="action",
        required=True,
        help="The specific action to be performed within the operation type",
    )

    parser.add_argument(
        "--api-key",
        dest="api_key",
        required=True,
        help="Firewall API key",
    )

    parser.add_argument(
        "--config",
        dest="config",
        default={},
        help=(
            "Python dictionary (as a string) for configuration settings for action. "
            "Should be a valid dictionary string. For example, use single quotes "
            "around the entire dictionary, double quotes around keys and values: "
            '\'{"key1": "value1", "key2": "value2"}\''
        ),
    )

    parser.add_argument(
        "--hostname",
        dest="hostname",
        required=True,
        help="Firewall hostname or IP",
    )

    parser.add_argument(
        "--log-level",
        dest="log_level",
        choices=LOGGING_LEVELS.keys(),
        default="debug",
        help="Set the logging output level",
    )

    parser.add_argument(
        "--type",
        dest="operation_type",
        choices=["readiness_check", "state_snapshot", "report"],
        required=True,
        help="The type of operation to be executed",
    )

    parser.add_argument(
        "--serial",
        dest="serial",
        required=False,
        help="Optional: serial of a Panorama managed firwall",
    )

    parser.add_argument(
        "--vsys",
        dest="vsys",
        required=False,
        help="Optional: vsys of remote firewall",
    )

    args = parser.parse_args()

    # Convert the config string to a dictionary
    if isinstance(args.config, str):
        try:
            args.config = ast.literal_eval(args.config)
        except Exception as e:
            parser.error(
                f"Argument --config: invalid dictionary provided: {args.config}\nError: {str(e)}"
            )

    # Return an instance of Args model
    return Args(
        hostname=args.hostname,
        api_key=args.api_key,
        operation_type=args.operation_type,
        action=args.action,
        config=args.config,
    )


# ----------------------------------------------------------------------------
# FirewallProxy object
# ----------------------------------------------------------------------------
def setup_firewall_proxy(hostname: str, api_key: str) -> FirewallProxy:
    """
    Create and return an instance of FirewallProxy.

    Args:
        hostname (str): Firewall hostname or IP
        api_key (str): Firewall API key

    Returns:
        FirewallProxy: FirewallProxy object
    """
    logging.debug(f"hostname: {hostname}")
    logging.debug(f"api_key: {api_key}")
    return FirewallProxy(hostname=hostname, api_key=api_key)


# ----------------------------------------------------------------------------
# Run operations
# ----------------------------------------------------------------------------
def run_assurance(
    hostname: str,
    api_key: str,
    operation_type: str,
    action: str,
    config: Dict[str, Union[str, int, float, bool]],
) -> Union[Dict[str, Union[str, int, float, bool]], None]:
    """
    Run a specified operation on the Firewall and return the result of the operation.

    Args:
        hostname (str): Firewall hostname or IP
        api_key (str): Firewall API key
        operation_type (str): Type of operation to be executed
        action (str): Specific action to be performed within the operation type
        config (dict): Configuration settings for action

    Returns:
        dict: Result of the operation
        None: If operation_type is invalid
    """
    # setup Firewall client
    firewall = setup_firewall_proxy(
        hostname=hostname,
        api_key=api_key,
    )

    results = None
    passed = True

    if operation_type == "readiness_check":
        if action not in READINESS_CHECKS:
            logging.error(f"Invalid action for readiness check: {action}")
            return
        logging.info(f"Performing readiness check: {action}")

        checks = CheckFirewall(firewall)

        # check if arp entry exists
        checks_configuration = [{action: config}]

        # run checks
        try:
            logging.info("Running readiness checks...")
            results = checks.run_readiness_checks(checks_configuration)
            logging.debug(results)
            for check in checks_configuration:
                check_name = list(check.keys())[0]
                passed = passed & results[check_name]["state"]

                if not results[check_name]["state"]:
                    logging.info(
                        "FAILED: %s - %s", check_name, results[check_name]["reason"]
                    )

        except Exception as e:
            logging.error("Error running readiness checks: %s", e)
            return

        logging.info("Completed checks successfully!")

    elif operation_type == "state_snapshot":
        actions = action.split(",")

        snapshot_node = CheckFirewall(firewall)

        # validate each type of action
        for each in actions:
            if each not in STATE_SNAPSHOTS:
                logging.error(f"Invalid action for state snapshot: {each}")
                return

        # take snapshots
        try:
            logging.info("Running snapshots...")
            results = snapshot_node.run_snapshots(snapshots_config=actions)
            logging.info(results)

        except Exception as e:
            logging.error("Error running readiness checks: %s", e)
            return

    elif operation_type == "report":
        if action not in REPORTS:
            logging.error(f"Invalid action for report: {action}")
            return
        logging.info(f"Generating report: {action}")
        # result = getattr(Report(firewall), action)(**config)

    else:
        logging.error(f"Invalid operation type: {operation_type}")
        return

    return results


# ----------------------------------------------------------------------------
# Main execution
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()

    print(args)

    # Configure logging
    logging.basicConfig(
        level=LOGGING_LEVELS[args.log_level],
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    # Look for config settings as argument, else empty dictionary
    config = args.config if args.config else {}

    # Run ARP entry assurance
    run_assurance(
        args.hostname,
        args.api_key,
        args.operation_type,
        args.action,
        config,
    )
