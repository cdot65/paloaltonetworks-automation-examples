# standard library imports
import os
import logging
import argparse
from typing import Any, Dict

# third party library imports
from dotenv import load_dotenv
from get_certificate_chain.download import SSLCertificateChainDownloader

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
        description="Retrieve certificate chain from host and upload to PAN-OS."
    )
    parser.add_argument(
        "--api-token",
        dest="api_key",
        default=PANTOKEN,
        help="Panorama API token (default: %(default)s)",
    )
    parser.add_argument(
        "--pan-url",
        dest="pan_url",
        default=PANURL,
        help="Panorama URL (default: %(default)s)",
    )
    parser.add_argument(
        "--host",
        dest="host",
        default="www.google.com",
        help="URL (default: %(default)s)",
    )
    return parser.parse_args()


# ----------------------------------------------------------------------------
# Retrieve certificate chain from host
# ----------------------------------------------------------------------------
def fetch_cert_chain(host: str) -> Dict[str, Any]:
    downloader = SSLCertificateChainDownloader(output_directory=f"/var/tmp/{host}")
    result = downloader.run({"host": host, "get_ca_cert_pem": True})
    if result and "files" in result:
        return result
    else:
        return {}


# ----------------------------------------------------------------------------
# Function to create and return an instance of Panorama
# ----------------------------------------------------------------------------
def setup_panorama_client(pan_url: str, api_key: str) -> panorama.Panorama:
    return panorama.Panorama(hostname=pan_url, api_key=api_key)


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def run_upload_cert_chain(pan_url: str, api_key: str, host: str) -> Dict[str, Any]:
    # Fetch the certificate chain
    cert_chain_files = fetch_cert_chain(host)

    # # Setup Panorama client
    # pan = setup_panorama_client(pan_url, api_key)

    # # Upload the certificates
    # for cert_file in cert_chain_files:
    #     with open(cert_file, "r") as f:
    #         certificate_data = f.read()

    #     # Extract certificate name from file
    #     cert_name = os.path.splitext(os.path.basename(cert_file))[0]

    #     print(f"cert_name: {cert_name}")
    #     # Add the certificate to Panorama
    #     pan.xapi.set(
    #         xpath=f"/config/shared/certificate/entry[@name='{cert_name}']",
    #         element=f"<certificate>\n{certificate_data}\n</certificate>",
    #     )

    return cert_chain_files


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_arguments()
    result = run_upload_cert_chain(
        args.pan_url,
        args.api_key,
        args.host,
    )
    logging.info(result)
