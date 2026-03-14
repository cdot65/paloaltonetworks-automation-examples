# Mock Panorama Server

## Overview

A placeholder project for a mock Palo Alto Networks Panorama management server API. Intended for testing PAN-OS automation scripts without requiring a live Panorama appliance. Once implemented, it will simulate the Panorama XML/REST API for local development and CI/CD pipelines. This project does not yet contain functional source code.

## Status

This project is a stub. No source files, endpoints, or runnable application exist yet. The directory contains only a Poetry lock file. Contributions welcome.

## Prerequisites

- Python 3.11+
- Poetry

## Quickstart

1. Clone the repository:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/panorama/mock-server
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```

   > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python, preventing version conflicts between projects.

3. Install dependencies:

   ```bash
   poetry install
   ```

4. No runnable application exists yet.

## Configuration

No configuration is required at this time.

## Usage

No usage instructions available. This project is a placeholder awaiting implementation.

### Expected Output

Not applicable -- no runnable code exists.

## Troubleshooting

| Problem | Solution |
|---|---|
| Connection refused | Not applicable -- no server is implemented yet |
| Invalid credentials | Not applicable |
| ModuleNotFoundError | Run `poetry install` to install dependencies |
| SSL certificate error | Not applicable |
| Timeout | Not applicable |
