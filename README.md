# Palo Alto Networks Automation Examples

## Overview

This repository contains dozens of examples demonstrating how to automate various aspects of Palo Alto Networks products. These examples cover a wide range of technologies and use cases, providing a valuable resource for network engineers, security professionals, and DevOps practitioners looking to streamline their Palo Alto Networks deployments and management tasks.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Technologies and Examples](#technologies-and-examples)
   - [Ansible](#ansible)
   - [Bash](#bash)
   - [Containers](#containers)
   - [Go](#go)
   - [Kubernetes](#kubernetes)
   - [Pulumi](#pulumi)
   - [Python](#python)
   - [Terraform](#terraform)
   - [TypeScript](#typescript)

## Project Structure

The repository is organized into the following main directories:

```
.
├── ansible/
├── bash/
├── containers/
├── go/
├── kubernetes/
├── pulumi/
├── python/
├── terraform/
└── typescript/
```

Each directory contains examples and projects related to the specific technology or tool. The `poetry.lock` and `pyproject.toml` files in the root directory suggest that Poetry is used for Python dependency management across the project.

## Technologies and Examples

### Ansible

Ansible is used for configuration management and automation of Palo Alto Networks devices.

**Key examples:**
- Deploying VM-Series firewalls on vCenter
- Dynamic inventory using Netbox
- Event-driven automation
- Content updates
- Creating address objects, security policies, and IPSec VPNs
- Firewall and Panorama configuration tasks

To explore Ansible examples, navigate to the `ansible/` directory.

### Bash

Bash scripts for various automation tasks related to Palo Alto Networks products.

To explore Bash examples, navigate to the `bash/` directory.

### Containers

This section includes container-related projects and execution environments.

**Key examples:**
- Event-driven Ansible container
- Execution environments for Nautobot, Netbox, and Palo Alto Networks
- PAN-OS Ansible container

To explore container examples, navigate to the `containers/` directory.

### Go

Go language examples for interacting with Palo Alto Networks devices.

**Key examples:**
- Firewall commit operations
- Clearing security counters
- Retrieving counters

To explore Go examples, navigate to the `go/` directory.

### Kubernetes

Kubernetes-related examples and configurations for Palo Alto Networks products.

**Key examples:**
- Helm chart for PAN-OS telemetry

To explore Kubernetes examples, navigate to the `kubernetes/` directory.

### Pulumi

Pulumi projects for infrastructure as code with Palo Alto Networks.

**Key examples:**
- Configuring BGP peers on PAN-OS devices

To explore Pulumi examples, navigate to the `pulumi/` directory.

### Python

Python scripts and projects for various Palo Alto Networks automation tasks.

**Key examples:**
- Configuring BGP peers, Panorama, and static DNS entries
- Global search and object search in PAN-OS
- Upgrade processes and assurance
- Prisma Access configuration
- ThreatVault hash lookups

To explore Python examples, navigate to the `python/` directory.

### Terraform

Terraform configurations for deploying and managing Palo Alto Networks infrastructure.

**Key examples:**
- Basic PAN-OS configuration
- Deploying VM-Series firewalls on VMware

To explore Terraform examples, navigate to the `terraform/` directory.

### TypeScript

TypeScript projects related to Palo Alto Networks automation.

**Key examples:**
- Saute project (details to be added)

To explore TypeScript examples, navigate to the `typescript/` directory.

## Getting Started

To get started with these examples:

1. Clone this repository
2. Navigate to the directory of the technology you're interested in
3. Follow the README or instructions within each example directory

## Contributing

We welcome contributions to this repository. Please read our contributing guidelines (link to be added) before submitting pull requests.

## License

This project is licensed under the terms specified in the `LICENSE` file in the root directory of this repository.
