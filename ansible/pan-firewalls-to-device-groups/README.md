# Palo Alto Networks Map Firewalls to Device Groups (filter plugin) 📚

This README provides an overview of our Ansible project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Palo Alto Networks Map Firewalls to Device Groups (filter plugin) 📚](#palo-alto-networks-map-firewalls-to-device-groups-filter-plugin-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Ansible](#installing-ansible)
  - [Inventory](#inventory)
  - [Playbook Structure](#playbook-structure)
  - [Custom Filter Plugins](#custom-filter-plugins)
    - [Creating Custom Filter Plugins](#creating-custom-filter-plugins)
    - [Using Custom Filter Plugins](#using-custom-filter-plugins)
    - [How the Filter Plugin Works](#how-the-filter-plugin-works)
    - [Calling the Custom Filter Plugin from the Playbook](#calling-the-custom-filter-plugin-from-the-playbook)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our Ansible project aims to automate the retrieval of device group information from a Panorama system based on the serial number of firewalls. By leveraging Ansible's powerful automation capabilities, including custom filter plugins, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.11+) 🐍
- pip (Python package manager) 📦

## Setup

### Creating a Python Virtual Environment

To create a Python virtual environment, follow these steps:

1. Open a terminal and navigate to the project directory.
2. Run the following command to create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - For Windows:

     ```bash
     venv\Scripts\activate
     ```

   - For macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

### Installing Ansible

With the virtual environment activated, install Ansible using pip:

```bash
pip install ansible
```

## Inventory

Our Ansible inventory file (`inventory.yaml`) defines the target hosts and groups for our playbook. If needed, you can adjust the inventory to match your environment. 📝

> **Note:** When using a Python virtual environment, make sure to specify the Python interpreter path in the inventory file:
>
> ```yaml
> all:
>   hosts:
>     localhost:
>       ansible_connection: local
>       ansible_python_interpreter: your_virtualenvironment/path/to/bin/python
> ```

Here is our inventory file content:

```yaml
all:
  children:
    panorama:
      hosts:
        panorama:
          ansible_host: 192.168.255.210
```

## Playbook Structure

Our Ansible playbook (`playbook.yaml`) is structured as follows:

```yaml
- name: Pull in Device Groups and Firewall relationships
  hosts: panorama
  connection: local
  gather_facts: false
  become: false
  vars:
    serial_number: "01234567890" # Example serial number

  tasks:
    - name: Pull in device group data from Panorama
      paloaltonetworks.panos.panos_op:
        provider:
          ip_address: "{{ ansible_host }}"
          username: "{{ panorama_credentials.username }}"
          password: "{{ panorama_credentials.password }}"
        cmd: "show devicegroups"
      register: results

    - name: Use Custom Filter to Find Device Group
      set_fact:
        device_group: "{{ results.stdout | from_json | find_device_group(serial_number) }}"

    - name: Print device group to console
      debug:
        var: device_group
```

The playbook consists of plays targeting specific hosts or groups. Variables can be defined at the playbook level. Tasks represent the actions to be performed on the target hosts. 🎭

## Custom Filter Plugins

This project introduces the concept of custom filter plugins for complex logic that is hard to achieve with standard YAML constructs.

### Creating Custom Filter Plugins

Custom filter plugins reside in the `filter_plugins` directory and allow for more advanced data manipulations and logic. Here is the Python code for our custom filter plugin:

```python
def find_device_group(data, serial_number):
    device_groups = (
        data.get("response", {})
        .get("result", {})
        .get("devicegroups", {})
        .get("entry", [])
    )

    for group in device_groups:
        devices_entry = group.get("devices", {}).get("entry", {})
        # Check if 'devices_entry' is a list and iterate through it
        if isinstance(devices_entry, list):
            for device in devices_entry:
                if device.get("@name") == serial_number:
                    return group.get("@name")
        # If 'devices_entry' is a dictionary, directly compare the serial number
        elif devices_entry.get("@name") == serial_number:
            return group.get("@name")

    return "Device group not found"


class FilterModule(object):
    """Custom filter to find device group"""

    def filters(self):
        return {"find_device_group": find_device_group}
```

### Using Custom Filter Plugins

To use the custom filter plugin, simply call it within the playbook as shown:

```yaml
- name: Use Custom Filter to Find Device Group
  set_fact:
    device_group: "{{ results.stdout | from_json | find_device_group(serial_number) }}"
```

### How the Filter Plugin Works

The custom filter plugin is a Python script that we use to handle more complex data transformations that are difficult to achieve solely with Ansible's YAML-based DSL. Here is a step-by-step explanation of how our plugin works:

1. **Data Extraction**:
    - The `find_device_group` function extracts the nested structure of device groups from the `data` dictionary. This extraction employs chained `get` methods to safely navigate and retrieve device group entries.

2. **Device Lookup**:
    - The function iterates through the list of device groups. For each group, it checks if the `devices` entry is a list or dictionary.
    - If `devices_entry` is a list, the function iterates through each device to check if the `@name` matches the given serial number.
    - If `devices_entry` is a dictionary, it directly checks if the `@name` key matches the serial number.

3. **Return Value**:
    - When a match is found, the function returns the name of the device group.
    - If no match is found, the function returns "Device group not found".

4. **FilterModule Class**:
    - This class allows Ansible to recognize the custom filter. The `filters` method returns a dictionary mapping the filter name (`find_device_group`) to the corresponding function.

### Calling the Custom Filter Plugin from the Playbook

In our playbook, it is straightforward to use this custom filter:

1. **Register the command output**:
    - The `paloaltonetworks.panos.panos_op` task runs a command to retrieve device groups from Panorama and registers the output in the variable `results`.

2. **Apply the Custom Filter**:
    - The `set_fact` task uses the custom `find_device_group` filter to parse the `results`, transforming it to JSON and then extracting the relevant device group based on the `serial_number`.

3. **Output the Result**:
    - The `debug` task prints the identified device group to the console.

Using a custom filter plugin, we can encapsulate complex logic in a concise and reusable Python function, making it significantly easier to handle advanced operations as compared to attempting the same directly within Ansible's YAML structure.

## Execution Workflow

To execute our Ansible playbook, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Run the following command:

   ```bash
   ansible-playbook -i inventory.yaml playbook.yaml
   ```

   This command specifies the inventory file (`inventory.yaml`) and the playbook file (`playbook.yaml`) to be executed.

3. Ansible will connect to the target hosts and execute the tasks defined in the playbook. 🚀

### Screenshots

Here are some screenshots showcasing the execution of our Ansible playbook:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄
