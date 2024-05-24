# standard library modules
import urllib3
import xml.etree.ElementTree as ET
from typing import List, Dict

# 3rd party modules
import requests
from config import settings

# Suppress only the single InsecureRequestWarning from urllib3 needed in this context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_config(xpath: str) -> str:
    """
    Fetch the current configuration from the specified API endpoint.

    :param xpath: XPath query for fetching the configuration.
    :return: Configuration XML as a string.
    """
    headers: Dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"}
    data: Dict[str, str] = {
        "key": settings.panos.apikey,
        "type": "config",
        "action": "get",
        "xpath": xpath,
    }
    response: requests.Response = requests.post(
        f"https://{settings.panos.hostname}/api",
        headers=headers,
        data=data,
        verify=False,
    )
    response.raise_for_status()
    return response.text


def update_config(
    xpath: str,
    dns_entry_xml: str,
) -> None:
    """
    Update the configuration with the new entry.

    :param xpath: XPath query for updating the configuration.
    :param dns_entry_xml: New entry XML to be added.
    """
    headers: Dict[str, str] = {"Content-Type": "application/x-www-form-urlencoded"}
    data: Dict[str, str] = {
        "key": settings.panos.apikey,
        "type": "config",
        "action": "set",
        "xpath": xpath,
        "element": dns_entry_xml,
    }
    response: requests.Response = requests.post(
        f"https://{settings.panos.hostname}/api",
        headers=headers,
        data=data,
        verify=False,
    )
    response.raise_for_status()


def create_new_entry(
    name: str,
    ip_address: str,
    domain_name: str,
) -> str:
    """
    Create a new entry XML string.

    :param name: Name of the new entry.
    :param ip_address: IP address of the new entry.
    :param domain_name: Domain name of the new entry.
    :return: New entry XML as a string.
    """
    entry_xml: str = (
        f'<entry name="{name}"><address><member>{ip_address}</member></address><domain>{domain_name}</domain></entry>'
    )
    return entry_xml


def main() -> None:
    """
    Main function to fetch, update, and print the configuration.
    """
    xpath: str = (
        f"/config/devices/entry[@name='localhost.localdomain']/network/dns-proxy/entry[@name='{settings.dns.domain}']/static-entries"
    )

    # Fetch current configuration
    config_xml: str = get_config(xpath)

    # Parse the XML response
    root: ET.Element = ET.fromstring(config_xml)

    # Extract existing DNS entries
    existing_entries: Dict[str, Dict[str, str]] = {}
    static_entries: ET.Element = root.find(".//static-entries")
    if static_entries is not None:
        for entry in static_entries.findall("entry"):
            name: str = entry.get("name")
            ip: str = entry.find("address/member").text
            domain: str = entry.find("domain").text
            existing_entries[name] = {"ip": ip, "domain": domain}

    # Track updated and skipped entries
    updated_entries: List[str] = []
    skipped_entries: List[str] = []

    for each in settings.dns.entries:
        if (
            each.name in existing_entries
            and existing_entries[each.name]["ip"] == each.ip
            and existing_entries[each.name]["domain"] == each.domain_name
        ):
            skipped_entries.append(
                f"- name: {each.name}\n  status: Entry is already in the intended state"
            )
        else:
            # Create new entry XML
            dns_entry_xml: str = create_new_entry(
                each.name,
                each.ip,
                each.domain_name,
            )

            # Update configuration
            update_config(
                xpath,
                dns_entry_xml,
            )

            updated_entries.append(
                f"- name: {each.name}\n  ip: {each.ip}\n  domain: {each.domain_name}"
            )

    # Print the YAML formatted list of updated and skipped DNS entries
    print("Updated DNS Entries:")
    print("\n".join(updated_entries))

    print("\nSkipped DNS Entries:")
    print("\n".join(skipped_entries))


if __name__ == "__main__":
    main()
