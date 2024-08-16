# Dynamic Inventory: Netbox 📚

This README provides an overview of our dynamic inventory project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Dynamic Inventory: Netbox 📚](#dynamic-inventory-netbox-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Inventory](#inventory)
  - [Dynamic Inventory Configuration](#dynamic-inventory-configuration)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our Ansible project aims to automate the configuration and deployment using inventory data fetched dynamically from Netbox via Ansible Controller or AWX. By leveraging Ansible's powerful automation capabilities and dynamic inventory, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.10 +) 🐍
- pip (Python package manager) 📦
- Ansible Controller or AWX installed ⚙️
- Ansible Galaxy collection for Netbox (`netbox.netbox`) 🌐
- Python dependencies: `pytz` and `pynetbox`

## Inventory

Our Ansible inventory is dynamically acquired from Netbox using the Netbox inventory plugin. This ensures that the inventory always reflects the current state of the managed infrastructure. 📝

## Dynamic Inventory Configuration

Here's the dynamic inventory configuration used to pull inventory data from Netbox:

```yaml
plugin: "netbox.netbox.nb_inventory"
api_endpoint: "http://netbox.netbox.svc.cluster.local"
token: "this-is-just-a-placeholder"
validate_certs: false
config_context: true
interfaces: true
group_names_raw: true
group_by:
  - device_roles
  - platforms
  - device_types
  - tenants
  - sites
  - racks
  - tags
query_filters: []
device_query_filters:
  - has_primary_ip: "true"
flatten_custom_fields: true
```

## Execution Workflow

To execute our dynamic inventory project, follow these steps:

1. Ensure that you have activated the Python virtual environment (use an execution environment like my personal instance [Netbox Execution Environment](https://github.com/users/cdot65/packages/container/package/ansible-ee-netbox)).
2. Ensure that the project has the dynamic inventory configuration properly set up.
3. Ansible will connect to Netbox to retrieve the inventory and then execute the tasks defined in the playbook. 🚀

### Screenshots

Here are some screenshots showcasing the execution of our Ansible playbook:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄
