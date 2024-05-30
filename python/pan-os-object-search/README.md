# pan-os-object-search 📚

This README provides an overview of our Python project and guides you through the setup and execution process. 🚀

## Table of Contents

- [pan-os-object-search 📚](#pan-os-object-search-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Dependencies](#installing-dependencies)
    - [Configuring Environment Variables](#configuring-environment-variables)
  - [Script Structure](#script-structure)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our Python project aims to automate the configuration and deployment of a search tool for address objects and their parent group associations in Palo Alto Networks' Panorama configurations. By leveraging Python's powerful automation capabilities, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.11+) 🐍
- pip (Python package manager) 📦

## Setup

### Creating a Python Virtual Environment

To create a Python virtual environment, follow these steps:

1. Open a terminal and navigate to the project directory.
2. Run the following command to create a virtual environment:

   ```console
   python -m venv venv
   ```

3. Activate the virtual environment:

   - For Windows:

     ```console
     venv\Scripts\activate
     ```

   - For macOS and Linux:

     ```console
     source venv/bin/activate
     ```

### Installing Dependencies

To install the required Python packages within our virtual environment, execute:

```console
pip install -r requirements.txt
```

### Configuring Environment Variables

Our script uses `dynaconf` for configuration management, and it is important to update both `settings.yaml` for the list of address objects to search on and `.secrets.yaml` for authentication. Create or update the following files in your project directory:

Create a file named `.secrets.yaml`:

```yaml
---
hostname: "panorama.example.com"
username: "your-username"
password: "your-password"
```

Create a file named `settings.yaml`:

```yaml
---
prefixes:
  - 1.1.1.1/32
  - 172.16.0.211
  - 172.16.0.2
```

## Script Structure

Our Python script (`pan-os-object-search.py`) is structured as follows:

```python
"""Search for instances of address objects and their associated parent groupings.

This script will locate all instances of an AddressObject within
the firewall's configuration.

(c) 2024 Calvin Remsburg
"""

# standard library imports
import argparse
import logging

# third party library imports
import pandas as pd
from tabulate import tabulate
from config import settings

# Palo Alto Networks imports
from panos.panorama import Panorama, DeviceGroup
from panos.objects import AddressObject, AddressGroup
from typing import Optional, Union


# ----------------------------------------------------------------------------
# Configure logging settings
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("search.log"), logging.StreamHandler()],
)

# ----------------------------------------------------------------------------
# Look in our settings.yaml and .secrets.yaml files to locate our credentials
# ----------------------------------------------------------------------------
pan = Panorama(
    hostname=settings.hostname,
    api_username=settings.username,
    api_password=settings.password,
)


# ----------------------------------------------------------------------------
# Function to grab Panorama configuration objects
# ----------------------------------------------------------------------------
def grab_config() -> tuple:
    """
    Description: collect configuration objects from Panorama.
    Workflow:
        1. Pull in various components of a Panorama configuration.
            - Device Groups
            - Address Groups
            - Address Objects
        2. Identify all address objects and append them to "address_objects"
        3. Identify all address groups and append them to "address_groups"
        4. Loop over device groups and perform steps 2 & 3 again.
    Return:
        - name: address_groups
          type: tuple
        - name: address_objects
          type: tuple
    """

    # inform user that we are retrieving configuration objects
    logging.debug("Retrieving Panorama configuration objects...")

    # load Panorama configuration objects
    pan_address_objects = AddressObject.refreshall(pan)
    pan_address_groups = AddressGroup.refreshall(pan)

    # create empty placeholders
    address_objects = []
    address_groups = []

    # append shared config address objects
    for each in pan_address_objects:
        address_objects.append(
            (
                "Shared",
                each.name,
                each.value,
                each.type,
            )
        )

    # append shared config address groups
    for each in pan_address_groups:
        if each.static_value:
            if not each.description:
                each.description = ""
            address_groups.append(
                (
                    "Shared",
                    each.name,
                    each.description,
                    each.static_value,
                )
            )

    # pull down list of device groups
    device_groups = DeviceGroup.refreshall(pan)

    # loop over device groups and perform the same actions
    for dg in device_groups:

        # start with address objects
        dg_address_objects = AddressObject.refreshall(dg)
        for each in dg_address_objects:
            address_objects.append(
                (
                    dg.name,
                    each.name,
                    each.value,
                    each.type,
                )
            )

        # finish with address groups
        dg_address_groups = AddressGroup.refreshall(dg)
        for each in dg_address_groups:
            if each.static_value:
                if not each.description:
                    each.description = ""
                address_groups.append(
                    (
                        dg.name,
                        each.name,
                        each.description,
                        each.static_value,
                    )
                )

    # return our address_groups and address_objects to the main function
    return address_groups, address_objects


# ----------------------------------------------------------------------------
# Function to map associations between address objects and their parent groups
# ----------------------------------------------------------------------------
def find_matches(
    address_groups: list,
    address_objects: list,
    search: str,
) -> Optional[Union[dict, None]]:
    """
    Description: Find all associations of an address object.
    Workflow:
        1. Loop over our address_objects and update `match` when the prefix is matched.
        2. Use the match's object name to see if it resides in an address_group object.
        3. Repeat for of the address group name to see if it's nested in another group.
    Return:
        - name: result
          type: Optional[Union[dict, None]]
    """

    # inform user that we are searching for a match
    logging.debug(f"Searching for matches of prefix: {search}")

    # create a placeholder for our potential match
    match = {}

    # loop over the address objects, update our match object if value is found
    for each in address_objects:
        if search in each:
            match["source"] = each[0]
            match["name"] = each[1]
            match["value"] = each[2]

    # if no match was found, return None
    if "name" not in match:
        return None

    # create a placeholder for our potential groups
    associations = []

    # loop over the address groups
    for each in address_groups:

        # if there is a positive match, then update our associations object
        if match["name"] in each[3]:
            associations.append(each)

    # let's finally loop over our associations object to see if a group is nested
    for each in associations:

        # loop over our address_groups object again, looking to find a match
        for group in address_groups:

            # append when we see the name of our address group matched in another address group
            if each[1] in group[3]:
                associations.append(group)

    # update match object with associations
    match["associations"] = associations

    return match


# ----------------------------------------------------------------------------
# Main execution of our script
# ----------------------------------------------------------------------------
def main():
    """
    Description: Main execution of our script.
    Workflow:
        1. Parse command-line arguments
        2. Set the logging level based on the provided argument
        3. Retrieve the list of prefixes from the settings.yaml file
        4. Call the `grab_config` function to retrieve configuration objects
        5. Loop over each prefix:
            a. Pass the prefix and lists objects into `find_matches`
            b. Print result to console
    """

    # create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Search for instances of address objects and their associated parent groupings."
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug logging"
    )
    args = parser.parse_args()

    # set the logging level based on the provided argument
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    # inform user that the script is starting
    logging.info("Script execution started.")

    # retrieve the list of prefixes from settings.yaml
    prefixes = settings.prefixes

    # pull in our configuration objects
    address_groups, address_objects = grab_config()

    # loop over each prefix
    for prefix in prefixes:
        # inform user that a search is taking place
        print(f"Searching for instances of {prefix}")

        # find all associations of the prefix
        match = find_matches(
            address_groups,
            address_objects,
            prefix,
        )

        # determine if the search was successful
        if match:

            # inform user that a match was found
            logging.debug(f"Match found for prefix: {prefix}")

            # check if there are any associations
            if match["associations"]:
                # create a pandas dataframe and print to the console.
                df = pd.DataFrame(match["associations"])
                print(
                    tabulate(
                        df,
                        headers="keys",
                        tablefmt="fancy_outline",
                    )
                )
            else:
                logging.debug(
                    f"Address object {match['name']} ({match['value']}) found but not in any address group."
                )
        else:
            logging.warning(f"No match was found for {prefix}")

        logging.info(f"Search completed for prefix: {prefix}")
        print()  # add an empty line between prefix results


# ----------------------------------------------------------------------------
# Execute main function
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
```

The script is designed to:

1. Load environment variables for Panorama credentials using `dynaconf`.
2. Retrieve configuration objects from Panorama.
3. Search for specified address objects and their associations.
4. Present the results in a tabulated format using `tabulate`.
5. Log activities and errors for debugging purposes.

## Execution Workflow

To execute our Python script, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

   ```console
   python pan-os-object-search.py
   ```

   To enable debug logging, use:

   ```console
   python pan-os-object-search.py --debug
   ```

### Screenshots

Here are some screenshots showcasing the execution of our Python script:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the script and customize it according to your specific requirements. Happy automating! 😄
