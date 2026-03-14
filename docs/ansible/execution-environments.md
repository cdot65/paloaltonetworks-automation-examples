# Execution Environments

Three custom Ansible Execution Environment (EE) container images built with `ansible-builder` for consistent, portable automation.

## What Are Execution Environments?

Execution Environments are container images that bundle Ansible, collections, Python dependencies, and system packages into a single portable unit. They ensure playbooks run identically across development, CI/CD, and production.

## Available EEs

### PAN-OS EE

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/execution-environments/ee-ansible)

Bundles `paloaltonetworks.panos` 2.17.0 and `pan-os-python` 1.11.0 for PAN-OS firewall and Panorama automation.

| Component | Version |
|-----------|---------|
| `paloaltonetworks.panos` | 2.17.0 |
| `pan-os-python` | 1.11.0 |
| `xmltodict` | included |

### Nautobot EE

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/execution-environments/ee-nautobot)

Built for automating Nautobot interactions with the `networktocode.nautobot` 4.1.1 collection and `pynautobot` SDK.

### NetBox EE

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/execution-environments/ee-netbox)

Built for automating NetBox interactions with the `netbox.netbox` 3.18.0 collection, `pynetbox`, and `pytz`.

## Building an EE

Each EE directory contains an `execution-environment.yml` definition file:

```bash
cd ansible/execution-environments/ee-ansible
ansible-builder build --tag pan-os-ee:latest
```
