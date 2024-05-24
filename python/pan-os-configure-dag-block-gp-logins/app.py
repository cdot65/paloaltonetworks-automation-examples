import logging
import requests
import sys
import time
import xml.etree.ElementTree as ET

from config import settings
from lxml import etree

# ------------------------------------------------------------------------------
# Configure logging
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


# ------------------------------------------------------------------------------
# Ask firewall for last 100 globalprotect logs with authentication failures
# ------------------------------------------------------------------------------
def create_job() -> str:
    """
    Create a job to fetch the last 100 GlobalProtect logs with authentication failures.

    Returns:
        str: Job ID if successful, None otherwise.
    """

    try:

        # Check if there are trusted users and construct the query part for them
        if settings.panos.trusted_users:
            trusted_users_query = " and ".join(
                [f"( user.src neq '{user}' )" for user in settings.panos.trusted_users]
            )
            query = f"( error eq 'Authentication failed: Invalid username or password' ) and {trusted_users_query}"

        else:
            query = "( error eq 'Authentication failed: Invalid username or password' )"

        # Construct the URL
        url = f"https://{settings.panos.hostname}/api/?key={settings.panos.apikey}&type=log&log-type=globalprotect&nlogs=100&query={query}"

        # Added timeout
        response = requests.get(url, timeout=10)

        # Raise an error for bad status codes
        response.raise_for_status()
        root = ET.fromstring(response.content)

        # Return the job ID
        return root.find(".//job").text

    # Catch exceptions and log them
    except requests.RequestException as e:
        logging.error(f"Network error occurred in check_job_status: {e}")
        return None

    # Catch XML parsing errors and log them
    except ET.ParseError as e:
        logging.error(f"XML parsing error occurred in check_job_status: {e}")
        return None


# ------------------------------------------------------------------------------
# Check for the status of the job
# ------------------------------------------------------------------------------
def check_job_status(job_id: str) -> str:
    """
    Check the status of a job.

    Args:
        job_id (str): The job ID to check.

    Returns:
        str: Job status.
    """

    # Construct the URL
    status_url = f"https://{settings.panos.hostname}/api/?key={settings.panos.apikey}&type=log&action=get&job-id={job_id}"

    # Get the status of the job
    response = requests.get(status_url)

    # Parse the XML and return the status
    root = ET.fromstring(response.content)

    # Return the status
    return root.find(".//job/status").text


# ------------------------------------------------------------------------------
# Retrieve and parse the results of the job
# ------------------------------------------------------------------------------
def get_job_results(job_id: str) -> bytes:
    """
    Retrieve the results of a job.

    Args:
        job_id (str): The job ID to retrieve results for.

    Returns:
        ElementTree: Parsed XML of job results if successful, None otherwise.
    """

    try:
        # Construct the URL
        result_url = f"https://{settings.panos.hostname}/api/?key={settings.panos.apikey}&type=log&action=get&job-id={job_id}"

        # Get the job results
        response = requests.get(result_url)

        # Raise an error for bad status codes
        response.raise_for_status()

        # Return the content
        return response.content

    except requests.RequestException as e:
        logging.error(f"Network error occurred in get_job_results: {e}")
        return None


# ------------------------------------------------------------------------------
# Extract the public IPs from the job results
# ------------------------------------------------------------------------------
def extract_public_ips(root: ET.Element) -> set:
    """
    Extract public IPs from the job results.

    Args:
        root (ElementTree): The root element of the job results XML.

    Returns:
        Set: A set of public IP addresses.
    """
    return set(
        entry.find("public_ip").text
        for entry in root.findall(".//entry")
        if entry.find("public_ip") is not None
    )


# ------------------------------------------------------------------------------
# Generate the XML file of DAG entries to add to the firewall
# ------------------------------------------------------------------------------
def generate_xml_file(public_ips: set, filename="dags.xml") -> str:
    """
    Generate an XML file containing DAG entries.

    Args:
        public_ips (Set[str]): A set of public IP addresses.
        filename (str, optional): The filename to write the XML to. Defaults to "dags.xml".

    Returns:
        str: The filename of the generated XML.
    """

    # Create the XML file
    uid_message = etree.Element("uid-message")

    # Add the type and payload elements
    etree.SubElement(uid_message, "type").text = "update"

    # Add the register element
    register = etree.SubElement(etree.SubElement(uid_message, "payload"), "register")

    # Add the tag elements
    for ip in public_ips:

        # Add the entry element
        member = etree.SubElement(
            etree.SubElement(etree.SubElement(register, "entry", ip=ip), "tag"),
            "member",
        )

        # Add the tag name
        member.text = settings.panos.dag_tag

    # Write the XML to a file
    tree = etree.ElementTree(uid_message)

    # Write the XML to a file
    tree.write(filename, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    # Return the filename
    return filename


# ------------------------------------------------------------------------------
# Send the generated XML file to the firewall
# ------------------------------------------------------------------------------
def send_xml_to_firewall(xml_filename: str) -> str:
    """
    Send an XML file to the firewall.

    Args:
        xml_filename (str): The filename of the XML to send.

    Returns:
        str: The response text from the firewall if successful, None otherwise.
    """

    # Send the XML file to the firewall
    try:

        # Construct the URL
        url = f"https://{settings.panos.hostname}/api/?type=user-id"

        # Send the XML file
        payload = {"key": settings.panos.apikey}

        # Open the file and send it
        with open(xml_filename, "rb") as file:

            # Construct the files parameter
            files = [("file", (xml_filename, file, "text/xml"))]

            # Send the request
            response = requests.request("POST", url, data=payload, files=files)

            # Raise an error for bad status codes
            response.raise_for_status()

        # Return the response text
        return response.text

    # Catch exceptions and log them
    except requests.RequestException as e:
        logging.error(f"Network or API error occurred in send_xml_to_firewall: {e}")
        return None

    # Catch file errors and log them
    except IOError as e:
        logging.error(f"File error in send_xml_to_firewall: {e}")
        return None


def main():
    """
    Main function to coordinate the process of fetching logs, processing them, and sending to the firewall.
    """

    # Create a job to fetch the last 100 GlobalProtect logs with authentication failures
    job_id = create_job()

    # If the job creation failed, log an error and exit
    if job_id is None:
        logging.error("Failed to create job. Exiting.")
        return

    # Check the status of the job until it is complete
    while True:

        # Check the status of the job
        status = check_job_status(job_id)

        # If the status is None, log an error and exit
        if status is None:
            logging.error("Failed to check job status. Exiting.")
            return

        # If the status is FIN, the job is complete
        if status == "FIN":
            logging.info("Job completed.")
            break

        # If the status is CAN, the job was canceled
        else:
            logging.info("Job still processing...")
            time.sleep(3)

    # Get the job results
    root_string = get_job_results(job_id)

    # If the job results are None, log an error and exit
    if root_string is None:
        logging.error("Failed to get job results. Exiting.")
        sys.exit(1)

    # Parse the job results
    try:
        root = ET.fromstring(root_string)
    except ET.ParseError as e:
        logging.error(f"XML parsing error occurred in get_job_results: {e}")
        sys.exit(1)

    # Extract the public IPs from the job results
    public_ips = extract_public_ips(root)

    # Generate the XML file of DAG entries to add to the firewall
    xml_filename = generate_xml_file(public_ips)

    # Send the generated XML file to the firewall
    response_text = send_xml_to_firewall(xml_filename)

    # Log the response text
    if response_text is None:
        logging.error("Failed to send XML to firewall. Exiting.")
        return

    # Log the response text
    logging.info(response_text)


if __name__ == "__main__":

    # Run the main function
    main()
