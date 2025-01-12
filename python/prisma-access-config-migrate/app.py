# standard library imports
import argparse
import logging
import sys
from typing import Dict, List, Tuple, Any

# Palo Alto Networks Prisma imports
from panapi import PanApiSession
from panapi.config.objects import Address, AddressGroup
from panapi.config.security import SecurityRule as PrismaSecurityRule

# third party library imports
from config import settings

# ----------------------------------------------------------------------------
# Configure logging
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ----------------------------------------------------------------------------
# Load environment variables from .secrets file
# ----------------------------------------------------------------------------
source_prisma_access = {
    "client_id": settings.oauth.source.client_id,
    "client_secret": settings.oauth.source.client_secret,
    "tenant": settings.oauth.source.tsg,
    "token_url": settings.oauth.token_url,
}
destination_prisma_access = {
    "client_id": settings.oauth.destination.client_id,
    "client_secret": settings.oauth.destination.client_secret,
    "tenant": settings.oauth.destination.tsg,
    "token_url": settings.oauth.token_url,
}


# ----------------------------------------------------------------------------
# Function to parse command line arguments
# ----------------------------------------------------------------------------
def parse_arguments():
    """
    Parse command line arguments.

    Parses the arguments provided to the script from the command line and returns them.

    Returns:
        argparse.Namespace: An argparse Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Parse arguments passed from Saute frontend."
    )
    parser.add_argument(
        "--config-objects",
        dest="config_objects",
        default="all",
        help="Comma-separated list of config objects to process (default: %(default)s). Options: address-objects, address-groups, security-rules, all",
    )
    return parser.parse_args()


# ----------------------------------------------------------------------------
# Function to filter rules that contain the specified tag
# ----------------------------------------------------------------------------
def filter_rules_by_tag(
    rules_data: List[Dict[str, Any]], tag: str
) -> List[Dict[str, Any]]:
    """
    Filter rules that contain the specified tag.

    Args:
        rules_data (List[Dict[str, Any]]): A list of rule data dictionaries.
        tag (str): The tag to filter rules by.

    Returns:
        List[Dict[str, Any]]: A list of rule data dictionaries that contain the specified tag.
    """
    filtered_rules_data = []
    for rule_data in rules_data:
        if "tag" in rule_data and tag in rule_data["tag"]:
            filtered_rules_data.append(rule_data)
    return filtered_rules_data


# ----------------------------------------------------------------------------
# Function to retrieve address objects and groups from the source tenant
# ----------------------------------------------------------------------------
def get_address_objects_and_groups(
    session: PanApiSession,
) -> Tuple[List[Address], List[AddressGroup]]:
    """
    Retrieve address objects and address groups from the source tenant.

    Args:
        session (PanApiSession): An authenticated PanApiSession for the source tenant.

    Returns:
        Tuple[List[Address], List[AddressGroup]]:
            A tuple containing a list of address objects and a list of address groups.
    """
    folder = {"folder": "Prisma Access"}

    source_address = Address(**folder)
    address_objects = source_address.list(session)

    source_address_groups = AddressGroup(**folder)
    address_groups = source_address_groups.list(session)

    return address_objects, address_groups


# ----------------------------------------------------------------------------
# Function to create Prisma address objects
# ----------------------------------------------------------------------------
def create_prisma_address_objects(
    address_objects: List[Address],
    session: PanApiSession,
) -> List[Dict[str, str]]:
    """
    Create address objects in the destination Prisma Access tenant.

    Iterates over the list of address objects from the source tenant,
    extracts necessary attributes, and creates corresponding address objects
    in the destination tenant.

    Args:
        address_objects (List[Address]): A list of address objects from the source tenant.
        session (PanApiSession): An authenticated PanApiSession for the destination tenant.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the created address objects.

    Raises:
        Exception: If there is an error creating an address object.
    """
    prisma_address_objects = []

    for address_object in address_objects:
        logging.debug(
            "Processing address_object: %s",
            address_object,
        )

        # Extract the necessary attributes
        prisma_address_data = {
            "name": address_object.name,
            "folder": "Prisma Access",
        }

        # Extract a description, if one exists
        if getattr(address_object, "description", None):
            prisma_address_data["description"] = address_object.description

        # Determine the type of address object and include the appropriate field
        if getattr(address_object, "ip_netmask", None):
            prisma_address_data["ip_netmask"] = address_object.ip_netmask
        elif getattr(address_object, "fqdn", None):
            prisma_address_data["fqdn"] = address_object.fqdn
        elif getattr(address_object, "ip_range", None):
            prisma_address_data["ip_range"] = address_object.ip_range
        else:
            logging.warning(
                "Address object %s has no valid address type.", address_object.name
            )
            continue  # Skip if there's no valid address type

        logging.debug("prisma_address_data: %s", prisma_address_data)

        try:
            prisma_address = Address(**prisma_address_data)
            prisma_address.create(session)
            prisma_address_objects.append(prisma_address_data)
        except Exception as e:
            logging.error("Error creating prisma address: %s", e)
            raise

    return prisma_address_objects


# ----------------------------------------------------------------------------
# Function to create Prisma address groups
# ----------------------------------------------------------------------------
def create_prisma_address_groups(
    address_groups: List[AddressGroup],
    session: PanApiSession,
) -> List[Dict[str, str]]:
    """
    Create address groups in the destination Prisma Access tenant.

    Iterates over the list of address groups from the source tenant,
    extracts necessary attributes, and creates corresponding address groups
    in the destination tenant.

    Args:
        address_groups (List[AddressGroup]): A list of address groups from the source tenant.
        session (PanApiSession): An authenticated PanApiSession for the destination tenant.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the created address groups.

    Raises:
        SystemExit: If there is an error creating an address group.
    """
    prisma_address_groups = []

    for address_group in address_groups:
        try:
            prisma_address_group_data = {
                "folder": "Prisma Access",
                "name": address_group.name,
            }

            # Add description if it exists
            if getattr(address_group, "description", None):
                prisma_address_group_data["description"] = address_group.description

            # Handle static address groups
            if getattr(address_group, "static", None):
                prisma_static_value = [name for name in address_group.static]
                prisma_address_group_data["static"] = prisma_static_value

            # Handle dynamic address groups
            if getattr(address_group, "dynamic", None):
                prisma_address_group_data["dynamic"] = {
                    "filter": address_group.dynamic["filter"]
                }

            prisma_address_group = AddressGroup(**prisma_address_group_data)
            prisma_address_group.create(session)
            prisma_address_groups.append(prisma_address_group_data)
        except Exception as e:
            logging.error("Error creating address group object: %s", e)
            sys.exit(1)

    return prisma_address_groups


# ----------------------------------------------------------------------------
# Function to create Prisma security rules
# ----------------------------------------------------------------------------
def create_prisma_security_rules(
    security_rules: Dict[str, Any],
    session: PanApiSession,
) -> List[Dict[str, str]]:
    """
    Create security rules in the destination Prisma Access tenant.

    Iterates over the security rules from the source tenant,
    and creates corresponding security rules in the destination tenant.

    Args:
        security_rules (Dict[str, Any]): A dictionary containing security rules categorized by device groups.
        session (PanApiSession): An authenticated PanApiSession for the destination tenant.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the created security rules.

    Raises:
        SystemExit: If there is an error creating a security rule.
    """
    prisma_security_rules = []

    for device_group, rulebases in security_rules.items():
        logging.debug("device_group: %s", device_group)
        logging.debug("rulebases: %s", rulebases)

        if len(rulebases["pre_rules"]) > 0:
            logging.debug("pre_rules: %s", rulebases["pre_rules"])
            for rule in rulebases["pre_rules"]:
                logging.debug("rule: %s", rule)
                try:
                    prisma_security_rule_data = {
                        "name": rule["rule_name"],
                        "folder": "Prisma Access",
                        "position": "pre",
                        "action": rule["actions"],
                        "from": ["any"],
                        "to": ["any"],
                        "source": ["any"],
                        "destination": ["any"],
                        "source_user": ["any"],
                        "category": ["any"],
                        "application": rule["applications"],
                        "service": ["any"],
                        "log_setting": "Cortex Data Lake",
                        "description": (
                            rule["description"] if rule["description"] else "n/a"
                        ),
                    }
                    prisma_security_rule = PrismaSecurityRule(
                        **prisma_security_rule_data
                    )
                    logging.debug("prisma_security_rule: %s", prisma_security_rule)
                    prisma_security_rule.create(session)
                    prisma_security_rules.append(prisma_security_rule_data)
                except Exception as e:
                    logging.error("Error creating security rule: %s", e)

        if len(rulebases["post_rules"]) > 0:
            logging.debug("post_rules: %s", rulebases["post_rules"])
            for rule in rulebases["post_rules"]:
                logging.debug("rule: %s", rule)
                try:
                    prisma_security_rule_data = {
                        "name": rule["rule_name"],
                        "folder": "Prisma Access",
                        "position": "post",
                        "action": rule["actions"],
                        "from": ["any"],
                        "to": ["any"],
                        "source": ["any"],
                        "destination": ["any"],
                        "source_user": ["any"],
                        "category": ["any"],
                        "application": rule["applications"],
                        "service": ["any"],
                        "log_setting": "Cortex Data Lake",
                        "description": (
                            rule["description"] if rule["description"] else "n/a"
                        ),
                    }
                    prisma_security_rule = PrismaSecurityRule(
                        **prisma_security_rule_data
                    )
                    logging.debug("prisma_security_rule: %s", prisma_security_rule)
                    prisma_security_rule.create(session)
                    prisma_security_rules.append(prisma_security_rule_data)
                except Exception as e:
                    logging.error("Error creating security rule: %s", e)
                    sys.exit(1)

    return prisma_security_rules


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def run_prisma_access_migrate(config_objects: str) -> Dict[str, Any]:
    """
    Main function to migrate configuration from source to destination Prisma Access tenant.

    Authenticates with both the source and destination Prisma Access tenants,
    retrieves the specified configuration objects from the source tenant,
    and creates them in the destination tenant.

    Args:
        config_objects (str): Comma-separated list of configuration objects to process.
            Options: 'address-objects', 'address-groups', 'security-rules', 'all'.

    Returns:
        Dict[str, Any]: A dictionary containing the results of the migration.
    """
    result = {}

    # Determine which config objects to process
    config_objects_list = [item.strip() for item in config_objects.split(",")]
    process_all = "all" in config_objects_list
    process_address_objects = process_all or "address-objects" in config_objects_list
    process_address_groups = process_all or "address-groups" in config_objects_list
    process_security_rules = process_all or "security-rules" in config_objects_list

    # Authenticate with source Prisma Access tenant
    try:
        source_session = PanApiSession()
        logging.info("Authenticating with source Prisma Access tenant...")

        source_session.authenticate(
            client_id=source_prisma_access["client_id"],
            client_secret=source_prisma_access["client_secret"],
            scope=f"profile tsg_id:{source_prisma_access['tenant']} email",
            token_url=source_prisma_access["token_url"],
        )
    except Exception as e:
        logging.error(f"Error with Prisma authentication: {e}")
        return {"error": str(e)}

    # Fetch address objects and groups from source
    address_objects = []
    address_groups = []
    if process_address_objects or process_address_groups:
        try:
            logging.info("Retrieving address objects and groups from source tenant...")
            address_objects, address_groups = get_address_objects_and_groups(
                source_session
            )
        except Exception as e:
            logging.error("Error retrieving address objects and groups: %s", e)
            sys.exit(1)

    # Authenticate with destination Prisma Access tenant
    try:
        destination_session = PanApiSession()
        logging.info("Authenticating with destination Prisma Access tenant...")

        destination_session.authenticate(
            client_id=destination_prisma_access["client_id"],
            client_secret=destination_prisma_access["client_secret"],
            scope=f"profile tsg_id:{destination_prisma_access['tenant']} email",
            token_url=destination_prisma_access["token_url"],
        )
    except Exception as e:
        logging.error(f"Error with destination Prisma authentication: {e}")
        return {"error": str(e)}

    # Create Prisma address objects
    if process_address_objects:
        try:
            logging.info(
                "Creating Prisma address objects in destination Prisma Access tenant..."
            )
            prisma_address_objects = create_prisma_address_objects(
                address_objects,
                destination_session,
            )
            result["prisma_address_objects"] = prisma_address_objects
        except Exception as e:
            logging.error(f"Error with Prisma API calls: {e}")
            return {"error": str(e)}

    # Create Prisma address groups
    if process_address_groups:
        try:
            logging.info(
                "Creating Prisma address groups in destination Prisma Access tenant..."
            )
            prisma_address_groups = create_prisma_address_groups(
                address_groups,
                destination_session,
            )
            result["prisma_address_groups"] = prisma_address_groups
        except Exception as e:
            logging.error(f"Error with Prisma API calls: {e}")
            return {"error": str(e)}

    return result


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_arguments()
    result = run_prisma_access_migrate(args.config_objects)
    logging.debug(result)
