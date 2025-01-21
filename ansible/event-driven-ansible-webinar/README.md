# Event-Driven Ansible Webinar 📚

This README provides an overview of our Event-Driven Ansible project and guides you through the setup, container build, execution process, and the configuration of log forwarding from Palo Alto Networks. 🚀

## Table of Contents

- [Event-Driven Ansible Webinar 📚](#event-driven-ansible-webinar-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Ansible](#installing-ansible)
    - [Building the Container Image](#building-the-container-image)
  - [Inventory](#inventory)
  - [Playbook Structure](#playbook-structure)
  - [Rulebook Structure](#rulebook-structure)
  - [Execution Workflow](#execution-workflow)
    - [Running the Container Using Invoke](#running-the-container-using-invoke)
    - [Screenshots](#screenshots)
  - [Configuring PAN-OS Log Forwarding](#configuring-pan-os-log-forwarding)
    - [HTTP Server Profile](#http-server-profile)
    - [Log Forwarding Profile](#log-forwarding-profile)

## Overview

Our Ansible project aims to automate the configuration and deployment of Event-Driven Ansible using a rulebook that reacts to specific conditions and executes playbooks accordingly. By leveraging this automation, we can ensure consistent and reproducible results across multiple environments. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Python (version 3.11) 🐍
- pip (Python package manager) 📦
- Ansible 🛠️
- Podman or Docker 🐳

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
pip install ansible ansible-runner ansible-rulebook pan-os-python xmltodict
```

### Building the Container Image

To build the container image, use the provided `invoke` script. This script determines whether to use Podman or Docker and builds the image accordingly.

1. Ensure the `invoke` library is installed:

   ```bash
   pip install invoke
   ```

2. Use the `invoke` command to build the container image:

   ```bash
   inv build
   ```

## Inventory

Our Ansible inventory file (`inventory.yaml`) defines the target hosts and groups for our playbook. For this project, the inventory is very simple:

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
```

## Playbook Structure

Our Ansible playbook (`playbook.yml`) is structured as follows:

```yaml
- name: Copy Certificates to Remote Hosts
  hosts: all
  gather_facts: false
  become: false
  tasks:
    - name: Collect System Facts
      ansible.builtin.setup:
      become: true

    - name: Send task to Ansible Automation Platform
      ansible.builtin.import_role:
        name: tls_remediation
```

The playbook defines tasks that will be executed on the target hosts, including roles for more complex tasks.

## Rulebook Structure

Our rulebook (`rulebook.yml`) is structured to define events, conditions, and actions:

```yaml
- name: "Receive logs sourced from HTTP Server Profile in PAN-OS"
  hosts: "localhost"

  sources:
    - paloaltonetworks.panos.logs:
        host: 0.0.0.0
        port: 5000
        type: decryption

  rules:
    - name: "Troubleshoot Decryption Failure"
      condition: event.meta.log_type == "decryption"
      action:
        run_playbook:
          name: "playbooks/decryption.yml"

    - name: "Slack Alert on DLP Violation"
      condition: event.meta.log_type == "data"
      action:
        run_playbook:
          name: "playbooks/send_slack_message.yml"

    - name: "ServiceNow Ticket on hardware failure"
      condition: event.meta.log_type == "system"
      action:
        run_playbook:
          name: "playbooks/create_snow_ticket.yml"
```

The rulebook listens for specific logs and executes playbooks based on the conditions defined.

## Execution Workflow

To execute our Ansible project, follow these steps:

1. Build and run the container using the `invoke` script:

   ```bash
   inv up
   ```

2. Tail the logs to monitor the execution:

   ```bash
   inv logs
   ```

3. To stop and remove the container:

   ```bash
   inv down
   ```

### Running the Container Using Invoke

1. **Ensure the `invoke` library is installed**:

   ```bash
   pip install invoke
   ```

2. **Build the container image**:

   ```bash
   inv build
   ```

3. **Run the container**:

   ```bash
   inv up
   ```

4. **Monitor the logs**:

   ```bash
   inv logs
   ```

5. **Stop and remove the container**:

   ```bash
   inv down
   ```

### Screenshots

Here are some screenshots showcasing the execution of our Ansible playbook:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

## Configuring PAN-OS Log Forwarding

To forward logs from Palo Alto Networks to Event-Driven Ansible (EDA), follow these steps:

### HTTP Server Profile

Create an HTTP Server Profile to define how the PAN-OS firewall should send events to the EDA server.

Example configuration:

```json
{
  "category": "network",
  "details": {
    "action": "$action",
    "app": "$app",
    "cn": "$cn",
    "dst": "$dst",
    "device_name": "$device_name",
    "error": "$error",
    "issuer_cn": "$issuer_cn",
    "root_cn": "$root_cn",
    "root_status": "$root_status",
    "sni": "$sni",
    "src": "$src",
    "srcuser": "$srcuser"
  },
  "receive_time": "$receive_time",
  "rule": "$rule",
  "rule_uuid": "$rule_uuid",
  "serial": "$serial",
  "sessionid": "$sessionid",
  "severity": "informational",
  "type": "decryption"
}
```

This profile can be configured using Ansible tasks in a playbook:

```yaml
- name: Create a HTTP Server Profile for Decryption Logs
  paloaltonetworks.panos.panos_http_profile:
    provider: '{{ device }}'
    name: '{{ server_profile_name_decrypt }}'
    decryption_name: 'decryption-logs-to-eda'
    decryption_uri_format: 'https://test'
    decryption_payload: >
      {
        "category": "network",
        "details": {
          "action": "$action",
          "app": "$app",
          "cn": "$cn",
          "dst": "$dst",
          "device_name": "$device_name",
          "error": "$error",
          "issuer_cn": "$issuer_cn",
          "root_cn": "$root_cn",
          "root_status": "$root_status",
          "sni": "$sni",
          "src": "$src",
          "srcuser": "$srcuser"
        },
        "receive_time": "$receive_time",
        "rule": "$rule",
        "rule_uuid": "$rule_uuid",
        "serial": "$serial",
        "sessionid": "$sessionid",
        "severity": "informational",
        "type": "decryption"
      }

- name: Create HTTP server
  paloaltonetworks.panos.panos_http_server:
    provider: '{{ device }}'
    http_profile: '{{ server_profile_name_decrypt }}'
    name: 'my-EDA-server'
    address: '192.168.1.5'
    http_method: 'GET'
    http_port: 5000

- name: Add a HTTP header to HTTP Server Profile
  paloaltonetworks.panos.panos_http_profile_header:
    provider: '{{ device }}'
    http_profile: '{{ server_profile_name_decrypt }}'
    log_type: 'decryption'
    header: 'Content-Type'
    value: 'application/json'

- name: Add a param to the config log type
  paloaltonetworks.panos.panos_http_profile_param:
    provider: '{{ device }}'
    http_profile: '{{ server_profile_name_decrypt }}'
    log_type: 'decryption'
    param: 'serial'
    value: '$serial'
```

### Log Forwarding Profile

Create a Log Forwarding Profile to filter for Decryption Logs and forward them to EDA.

Example configuration:

```yaml
- name: Create log forwarding profile
  paloaltonetworks.panos.panos_log_forwarding_profile:
    provider: '{{ provider }}'
    name: 'EDA_LFP'
    enhanced_logging: true

- name: Create log forwarding profile match list
  paloaltonetworks.panos.panos_log_forwarding_profile_match_list:
    provider: '{{ provider }}'
    log_forwarding_profile: 'EDA_LFP'
    name: 'eda-decryption-forwarding'
    log_type: 'decryption'
    filter: '( err_index neq None ) and ( proxy_type eq Forward )'
    http_profiles: ['{{ server_profile_name_decrypt }}']
```

With these configurations, logs from the PAN-OS firewall will be forwarded to the EDA server, where they can be processed and trigger the appropriate playbooks defined in the rulebook.

Feel free to explore the playbook and customize it according to your specific requirements. Happy automating! 😄
