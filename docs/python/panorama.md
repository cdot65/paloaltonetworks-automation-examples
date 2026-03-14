# Panorama Python Tools

7 Python projects for Panorama centralized management, from address object provisioning to sync status reporting.

## Projects

| Project | Description |
|---------|-------------|
| [configure-address-objects](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panorama/configure-address-objects) | CLI tool that reads IP-netmask address objects from YAML, validates with Pydantic, and pushes to Panorama device groups with optional auto-commit and push. |
| [configure-logical-interfaces](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panorama/configure-logical-interfaces) | Creates tunnel interfaces under Templates and loopback interfaces under Template Stacks from YAML config, supporting PAN-OS template variables. |
| [configure-settings](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panorama/configure-settings) | Comprehensive config-as-code tool that bulk-provisions tags, addresses, groups, services, applications, and application tags across device groups from deep-merged YAML files. |
| [log-pull](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panorama/log-pull) | Two-script toolkit that pulls traffic logs second-by-second over a configurable time range and converts raw XML responses to CSV with 100+ column mapping. |
| [object-search](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panorama/object-search) | Searches address objects across all device groups and maps their membership in address groups (including nested), rendering tables with pandas and tabulate. |
| [sync-report](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panorama/sync-report) | Queries device group and template sync status via XML API and generates a color-coded PDF report (green = in sync, red = out of sync) using ReportLab. |
| [mock-server](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panorama/mock-server) | *Placeholder* -- intended to simulate the Panorama XML/REST API for local testing. Not yet implemented. |
