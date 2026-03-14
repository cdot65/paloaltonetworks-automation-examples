# Panorama Ansible Playbooks

6 playbooks for centralized management tasks on Panorama including content updates, address objects, upgrades, and dynamic inventory integration.

## Projects

| Project | Description |
|---------|-------------|
| [content-update](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panorama/content-update) | Downloads the latest App+Threats and Antivirus updates on Panorama, polling async job status with retries at 30-second intervals. |
| [create-address-object](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panorama/create-address-object) | Creates FQDN-based address objects on Panorama with check mode validation before committing. |
| [dynamic-inventory-netbox](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panorama/dynamic-inventory-netbox) | Configures the `netbox.netbox.nb_inventory` plugin to dynamically pull device data and group hosts by role, platform, site, and tags. |
| [firewalls-to-device-groups](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panorama/firewalls-to-device-groups) | Queries Panorama with `show devicegroups` and uses a custom Python filter plugin to map serial numbers to device group names. |
| [hello-world](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panorama/hello-world) | A minimal playbook demonstrating Ansible basics (variables, tags, handlers) with no external dependencies. |
| [upgrade](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panorama/upgrade) | Automates the full PAN-OS upgrade lifecycle (download, install, restart) for a Panorama-managed firewall by serial number. |
