# standard library imports
import logging
import argparse
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

# third party library imports
from environs import Env
import xml.etree.ElementTree as ET
import xmltodict
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Palo Alto Networks PAN-OS imports
from panos.panorama import Panorama

# ----------------------------------------------------------------------------
# Configure logging
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------------------------------------------------------------------
# Load environment variables from .env file
# ----------------------------------------------------------------------------
env = Env()
env.read_env()

pan_config = {
    "pan_url": env("PANURL", "panorama.cdot.io"),
    "api_key": env("PANTOKEN", "supersecret"),
}


# ----------------------------------------------------------------------------
# Define data models
# ----------------------------------------------------------------------------
class RoleBased(BaseModel):
    superuser: Optional[str]
    panorama_admin: Optional[str]
    superreader: Optional[str]


class Permissions(BaseModel):
    role_based: Optional[RoleBased]


class Entry(BaseModel):
    name: str = Field(alias="@name")
    phash: str
    permissions: Permissions


class Users(BaseModel):
    entry: List[Entry]


class Result(BaseModel):
    total_count: int = Field(alias="@total-count")
    count: int = Field(alias="@count")
    users: Users


class Response(BaseModel):
    status: str = Field(alias="@status")
    code: str = Field(alias="@code")
    result: Result


class AdminList(BaseModel):
    response: Response


# ----------------------------------------------------------------------------
# Function to parse command line arguments
# ----------------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Retrieve list of administrators from Panorama."
    )
    parser.add_argument(
        "--pan-url",
        dest="pan_url",
        default=pan_config["pan_url"],
        help="Panorama URL (default: %(default)s)",
    )
    parser.add_argument(
        "--pan-token",
        dest="api_key",
        default=pan_config["api_key"],
        help="Panorama API token (default: %(default)s)",
    )
    parser.add_argument(
        "--to-emails",
        dest="to_emails",
        default=env("TO_EMAILS", "to@example.com"),
        help="Recipient email address (default: %(default)s)",
    )
    parser.add_argument(
        "--sendgrid-api-key",
        dest="sendgrid_api_key",
        default=env("SENDGRID_API_KEY"),
        help="SendGrid API key (default: %(default)s)",
    )
    return parser.parse_args()


# ----------------------------------------------------------------------------
# Function to create and return an instance of Panorama
# ----------------------------------------------------------------------------
def setup_panorama_client(pan_url: str, api_key: str) -> Panorama:
    logging.debug(f"pan_url: {pan_url}")
    logging.debug(f"api_key: {api_key}")
    return Panorama(hostname=pan_url, api_key=api_key)


# ----------------------------------------------------------------------------
# Function to fetch administrators
# ----------------------------------------------------------------------------
def get_administrators(pan: Panorama) -> AdminList:
    admin_list = pan.xapi.get(xpath="/config/mgt-config/users")
    xml_str = ET.tostring(admin_list, encoding="utf-8").decode("utf-8")
    data = xmltodict.parse(xml_str)

    admins = AdminList(**data)
    return admins


# ----------------------------------------------------------------------------
# Function to convert result into pandas DataFrame and then into HTML table
# ----------------------------------------------------------------------------
def convert_to_html_table(result: Dict[str, Any]) -> str:
    # Convert the list of Entry objects into a DataFrame
    df = pd.DataFrame(result["response"]["result"]["users"]["entry"])

    # Drop the phash column
    df = df.drop(columns=["phash", "permissions"])

    # Convert the DataFrame into an HTML table with bootstrap styled classes
    html_table = df.to_html(classes="table table-striped table-hover")

    # Wrap the HTML with bootstrap CSS from a CDN
    styled_html_table = f"""
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    {html_table}
    """

    return styled_html_table


# ----------------------------------------------------------------------------
# Function to send an email with the HTML table
# ----------------------------------------------------------------------------
def send_email(html_content: str, to_emails: str, sendgrid_api_key: str):
    header = "<h1>Admin Report</h1>"
    body = "<p>Dear Team,</p><p>Please find the latest admin report attached below:</p>"
    footer = "<p>Best regards,<br/>Your Admin Team</p>"

    message = Mail(
        from_email="calvin@redtail.consulting",
        to_emails=to_emails,
        subject="Panorama Administrators",
        html_content=f"{header}{body}{html_content}{footer}",
    )
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def run_admin_report(
    pan_url: str,
    api_key: str,
    to_emails: str,
    sendgrid_api_key: str,
) -> Dict[str, Any]:
    # authenticate with Panorama
    logging.info("Authenticating with Panorama...")
    pan = setup_panorama_client(pan_url, api_key)
    logging.debug(pan)

    # fetch administrators
    try:
        logging.info("Retrieving administrators...")
        admins = get_administrators(pan)
    except Exception as e:
        logging.error("Error retrieving administrators: %s", e)
        return

    logging.info("Completed job successfully!")
    logging.debug("admins: \n%s", admins.dict())

    # Convert the result into an HTML table
    html_table = convert_to_html_table(admins.dict())
    logging.debug("html_table: \n%s", html_table)

    # Send the HTML table as an email
    send_email(html_table, to_emails, sendgrid_api_key)

    return admins.dict()


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_arguments()
    result = run_admin_report(
        args.pan_url,
        args.api_key,
        args.to_emails,
        args.sendgrid_api_key,
    )
    logging.debug(result)
