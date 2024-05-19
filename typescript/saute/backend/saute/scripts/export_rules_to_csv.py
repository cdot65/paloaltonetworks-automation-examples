# standard library imports
import os
import csv
import datetime
import logging
import argparse
from typing import List, Tuple

# third party library imports
from dotenv import load_dotenv

# Palo Alto Networks imports
from panos import panorama
from panos.policies import PreRulebase, PostRulebase, SecurityRule

# ----------------------------------------------------------------------------
# Load environment variables from .env file
# ----------------------------------------------------------------------------
load_dotenv(".env")
PANURL = os.environ.get("PANURL", "panorama.lab.com")
PANTOKEN = os.environ.get("PANTOKEN", "mysecretpassword")

# ----------------------------------------------------------------------------
# Load environment variables from .env file
# ----------------------------------------------------------------------------
TIMESTAMP = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
OUTPUT_FILE = f"panorama_rules_{TIMESTAMP}.csv"


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
# Function to retrieve security rules and associated Security Profile Groups
# ----------------------------------------------------------------------------
def get_security_rules_and_profiles(pan: panorama.Panorama) -> List[Tuple[str, str]]:
    # Create Pre Rulebase and Post Rulebase instances
    pre_rulebase = PreRulebase()
    post_rulebase = PostRulebase()

    # Add Pre Rulebase and Post Rulebase to the Panorama instance
    pan.add(pre_rulebase)
    pan.add(post_rulebase)

    # Retrieve Pre Rules and Post Rules
    pre_rules = SecurityRule.refreshall(pre_rulebase)
    post_rules = SecurityRule.refreshall(post_rulebase)

    # Combine Pre Rules and Post Rules
    rules = pre_rules + post_rules

    # Prepare data
    data = []
    for rule in rules:
        security_profile_group = rule.group
        data.append(
            (rule.name, security_profile_group if security_profile_group else "N/A")
        )

    return data


# ----------------------------------------------------------------------------
# Function to save data to a CSV file
# ----------------------------------------------------------------------------
def save_to_csv(data: List[Tuple[str, str]], filename: str) -> None:
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["RuleName", "SecurityProfileGroup"])
        writer.writerows(data)


# ----------------------------------------------------------------------------
# Function to get the output filepath
# ----------------------------------------------------------------------------
def get_output_filepath(filename: str) -> str:
    output_directory = os.path.dirname(filename)
    if not output_directory:
        output_directory = os.getcwd()
    os.makedirs(output_directory, exist_ok=True)
    return os.path.join(output_directory, filename)


# ----------------------------------------------------------------------------
# Configure logging
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def run_export_rules_to_csv(pan_url: str, api_key: str) -> None:
    pan = panorama.Panorama(hostname=pan_url, api_key=api_key)

    try:
        # Get security rules and associated Security Profile Groups
        data = get_security_rules_and_profiles(pan)
    except Exception as e:
        logging.error(f"Error retrieving security rules: {e}")
        return

    # Get the output filepath
    output_filepath = get_output_filepath(OUTPUT_FILE)

    try:
        # Save the data to a CSV file
        save_to_csv(data, output_filepath)
    except Exception as e:
        logging.error(f"Error saving data to CSV file: {e}")
        return

    logging.info(f"Exported to {output_filepath}")
    return output_filepath


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    args = parse_arguments()
    run_export_rules_to_csv(args.pan_url, args.api_key)
