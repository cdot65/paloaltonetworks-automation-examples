"""Search for instances of words within a live PAN-OS firewall's XML configuration.

This script will retrieve the full XML configuration from a live PAN-OS firewall,
then locate all instances of specified words within the configuration,
providing XPath, entry name, and full YAML configuration for each match.

(c) 2024 Calvin Remsburg
"""

# standard library imports
import argparse
import json
import logging
import warnings
from typing import List, Tuple

# third party library imports
import requests
import xmltodict
import yaml
from lxml import etree
from tabulate import tabulate
from urllib3.exceptions import InsecureRequestWarning

from config import settings

# Suppress only the single InsecureRequestWarning from urllib3
warnings.filterwarnings('ignore', category=InsecureRequestWarning)

# ----------------------------------------------------------------------------
# Configure logging settings
# ----------------------------------------------------------------------------
logger = logging.getLogger(__name__)


def configure_logging(debug: bool = False) -> None:
    """Configure logging settings."""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("search.log"), logging.StreamHandler()],
    )


# ----------------------------------------------------------------------------
# Firewall configuration retrieval
# ----------------------------------------------------------------------------
def get_firewall_config() -> str:
    """Retrieve the full XML configuration from the live PAN-OS firewall."""
    url = f"https://{settings.hostname}/api/?type=op&cmd=<show><config><merged></merged></config></show>"
    headers = {
        'X-PAN-KEY': settings.api_key
    }

    logger.info(f"Retrieving configuration from {settings.hostname}")
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        logger.info("Configuration retrieved successfully")
        return response.text
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve configuration: {e}")
        raise


# ----------------------------------------------------------------------------
# XML parsing and searching functions
# ----------------------------------------------------------------------------
def get_xpath(element: etree._Element) -> str:
    """Generate the XPath of the given element."""
    components = []
    while element is not None and element.getparent() is not None:
        siblings = element.getparent().xpath(f'./{element.tag}')
        index = siblings.index(element) + 1
        components.append(f'{element.tag}[{index}]')
        element = element.getparent()
    components.reverse()
    return '/' + '/'.join(components)


def get_entry_name(element: etree._Element) -> str:
    """Get the name of the entry containing the element."""
    entry = element.xpath("./ancestor-or-self::entry[1]")
    if entry:
        return entry[0].get('name', 'No name found')
    return 'Not within an entry'


def get_full_xml(element: etree._Element) -> str:
    """Get the full XML configuration of the object containing the match."""
    ancestor = element.xpath("./ancestor-or-self::entry[1]")
    if not ancestor:
        ancestor = [element.getroottree().getroot()]
    return etree.tostring(ancestor[0], pretty_print=True, encoding='unicode')


def xml_to_yaml(xml_string: str) -> str:
    """Convert XML string to YAML string."""
    xml_dict = xmltodict.parse(xml_string)
    json_str = json.dumps(xml_dict)
    json_dict = json.loads(json_str)
    return yaml.dump(json_dict, default_flow_style=False)


def search_for_words(root: etree._Element, words: List[str]) -> List[Tuple[str, str, str, str]]:
    """Search for all instances of the words in the text nodes and attribute values of the XML tree."""
    results = []
    for word in words:
        logger.debug(f"Searching for word: {word}")
        for element in root.xpath(f'//*[contains(text(), "{word}") or @*[contains(., "{word}")]]'):
            xpath = get_xpath(element)
            if not xpath.startswith('/shared/content-preview/application/entry/description'):
                entry_name = get_entry_name(element)
                full_xml = get_full_xml(element)
                full_yaml = xml_to_yaml(full_xml)
                results.append((xpath, entry_name, full_yaml, word))
                logger.debug(f"Match found: {xpath}")
    return results


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def main():
    """Main execution of the script."""
    parser = argparse.ArgumentParser(
        description="Search for words in the live PAN-OS firewall's XML configuration and print the full XPath, entry name, and full YAML configuration of each result."
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug logging"
    )
    args = parser.parse_args()

    configure_logging(args.debug)
    logger.info("Script execution started.")

    try:
        xml_config = get_firewall_config()
        root = etree.fromstring(xml_config)
    except (requests.RequestException, etree.XMLSyntaxError) as e:
        logger.error(f"Error retrieving or parsing XML configuration: {e}")
        return

    words = settings.keywords
    logger.info(f"Searching for words: {', '.join(words)}")

    results = search_for_words(root, words)

    if results:
        table_data = [[i + 1, result[3], result[1], result[0]] for i, result in enumerate(results)]
        headers = ["No.", "Matched Word", "Entry Name", "XPath"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        logger.info(f"Found {len(results)} matches.")
        print("\nDetailed Results:")
        print("=" * 80)

        for i, (xpath, entry_name, full_yaml, word) in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Matched Word: {word}")
            print(f"XPath: {xpath}")
            print(f"Entry Name: {entry_name}")
            print("Full YAML Configuration:")
            print(full_yaml)
            print("-" * 80)
    else:
        logger.info("No matches found.")

    logger.info("Search completed.")


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
