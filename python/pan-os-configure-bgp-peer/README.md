# pan-configure-bgp-peer 📚

This README provides an overview of our Python project and guides you through the setup and execution process. 🚀

## Table of Contents

- [pan-configure-bgp-peer 📚](#pan-configure-bgp-peer-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Creating a Python Virtual Environment](#creating-a-python-virtual-environment)
    - [Installing Dependencies](#installing-dependencies)
  - [Script Structure](#script-structure)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our Python project aims to automate the configuration and deployment of BGP peers on PAN-OS firewalls. By leveraging `pan-os-python`, an object-oriented SDK provided by Palo Alto Networks, and `Dynaconf` for configuration management, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

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

### Installing Dependencies

To install the necessary Python packages within our virtual environment, use the following command:

   ```bash
   pip install -r requirements.txt
   ```

Ensure your `requirements.txt` file includes the following dependencies:

```txt
pan-os-python==1.11.0
dynaconf==3.2.1
```

## Script Structure

Our Python script (`app.py`) is structured as follows:

```python

from panos.firewall import Firewall
from panos.network import VirtualRouter, Bgp, BgpPeer, BgpPeerGroup
from config import settings

firewall = Firewall(
    settings.hostname,
    api_username=settings.username,
    api_password=settings.password,
)

dc_vr = VirtualRouter(name=settings.vr_name)
firewall.add(dc_vr)

dc_bgp = Bgp(
    enable=True,
    router_id=settings.router_id,
    local_as=settings.local_as,
)
dc_vr.add(dc_bgp)
dc_bgp.apply()

dc_bgp_peer_group = BgpPeerGroup(
    enable=True,
    soft_reset_with_stored_info=True,
    type="ebgp",
    name=settings.bgp_name,
)
dc_bgp.add(dc_bgp_peer_group)

for each in settings.neighbors:
    each_bgp_peer = BgpPeer(
        name=each.name,
        enable=True,
        peer_as=each.asn,
        address_family_identifier="ipv4",
        local_interface=each.iface,
        local_interface_ip=each.local_ip,
        peer_address_ip=each.peer_ip,
    )
    dc_bgp_peer_group.add(each_bgp_peer)

    each_bgp_peer.apply()
```

The script configures a BGP peer on a PAN-OS firewall by:

1. Connecting to the firewall using provided credentials.
2. Adding a virtual router.
3. Enabling BGP on the virtual router with specified settings.
4. Creating a BGP Peer Group.
5. Adding BGP peers to the peer group based on the configuration in `settings.yaml`.

## Execution Workflow

To execute our Python script, follow these steps:

1. Ensure that you have activated the Python virtual environment.
2. Update the `settings.yaml` and `.secrets.yaml` files to match your environment requirements.
3. Run the following command:

   ```bash
   python app.py
   ```

### Screenshots

Here are some screenshots showcasing the execution of our Python script:

![Screenshot 1](screenshots/screenshot1.png)

![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the script and customize it according to your specific requirements. Happy automating! 😄
