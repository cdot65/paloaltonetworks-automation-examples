# PAN-OS Upgrade Automation

## Overview

This directory is a reference to the standalone `pan-os-upgrade` project hosted at [github.com/cdot65/pan-os-upgrade](https://github.com/cdot65/pan-os-upgrade). It is a CLI tool for automating configuration backups, network state snapshots, readiness checks, and operating system upgrades of Palo Alto Networks firewalls and Panorama appliances. It supports individual firewall upgrades, individual Panorama upgrades, and batch upgrades of multiple firewalls through a Panorama appliance. No source code is included in this directory.

**Note:** This is a placeholder directory pointing to an external project. See the links below for full documentation and source code.

## Prerequisites

- Python 3.8+
- Network access to PAN-OS firewalls or Panorama
- Valid credentials (username/password) for target devices

## Quickstart

1. Install the package from PyPI:

    ```bash
    pip install pan-os-upgrade
    ```

    > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python and other projects. This prevents version conflicts and ensures reproducibility. Consider creating one with `python3 -m venv .venv && source .venv/bin/activate` before installing.

2. Upgrade a single firewall (interactive prompts for hostname, credentials, and target version):

    ```bash
    pan-os-upgrade firewall
    ```

## Usage

Upgrade a single firewall:

```bash
pan-os-upgrade firewall
```

Upgrade a Panorama appliance:

```bash
pan-os-upgrade panorama
```

Batch upgrade firewalls through Panorama:

```bash
pan-os-upgrade batch
```

Each command interactively prompts for hostname, credentials, and target version.

## Documentation

- Full documentation: [https://cdot65.github.io/pan-os-upgrade/](https://cdot65.github.io/pan-os-upgrade/)
- Source code: [https://github.com/cdot65/pan-os-upgrade](https://github.com/cdot65/pan-os-upgrade)
- Docker instructions are available in the documentation site.
