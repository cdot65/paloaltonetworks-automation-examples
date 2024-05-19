# standard library imports
import os
import json
import logging
import argparse
from typing import Any, Dict

# third party library imports
import xmltodict
from xml.etree.ElementTree import tostring
from dotenv import load_dotenv

# Palo Alto Networks imports
from panos import panorama


# ----------------------------------------------------------------------------
# Configure logging
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


# ----------------------------------------------------------------------------
# Load environment variables from .env file
# ----------------------------------------------------------------------------
load_dotenv(".env")
PANURL = os.environ.get("PANURL", "panorama.lab.com")
PANTOKEN = os.environ.get("PANTOKEN", "mysecretpassword")


# ----------------------------------------------------------------------------
# Function to parse command line arguments
# ----------------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Export security rules and associated Security Profile Groups to a CSV file."
    )
    parser.add_argument(
        "--pan-url",
        dest="pan_url",
        default=PANURL,
        help="Panorama URL (default: %(default)s)",
    )
    parser.add_argument(
        "--pan-pass",
        dest="api_key",
        default=PANTOKEN,
        help="Panorama password (default: %(default)s)",
    )
    return parser.parse_args()


# ----------------------------------------------------------------------------
# Function to create and return an instance of Panorama
# ----------------------------------------------------------------------------
def setup_panorama_client(pan_url: str, api_key: str) -> panorama.Panorama:
    return panorama.Panorama(hostname=pan_url, api_key=api_key)


# ----------------------------------------------------------------------------
# Function to run our command
# ----------------------------------------------------------------------------
def fetch_system_information(pan: panorama.Panorama) -> Dict[str, Any]:
    system_info = pan.op("show system info")
    xml_string = tostring(system_info).decode(
        "utf-8"
    )  # Convert the Element object to a string
    xml_dict = xmltodict.parse(
        xml_string
    )  # Parse the XML string to a Python dictionary
    return json.loads(json.dumps(xml_dict))  # Convert the Python dictionary to JSON


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def run_get_system_info(pan_url: str, api_key: str) -> Dict[str, Any]:
    pan = setup_panorama_client(pan_url, api_key)

    try:
        system_info = fetch_system_information(pan)
    except Exception as e:
        logging.error(f"Error fetching system information: {e}")
        return {"error": str(e)}

    logging.info(f"Retrieved system information: {system_info}")
    return system_info


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_arguments()
    result = run_get_system_info(args.pan_url, args.api_key)
    logging.info(result)
