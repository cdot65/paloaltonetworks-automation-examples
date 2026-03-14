# PAN-OS Ansible Playbooks

11 playbooks for automating PAN-OS firewall configuration, security policies, VPN setup, certificate management, and log retrieval.

## Projects

### Configuration & Provisioning

| Project | Description |
|---------|-------------|
| [create-config-and-load](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/create-config-and-load) | Generates a complete PAN-OS XML config from Jinja2 templates and per-host variables, then uploads and loads it via the REST API using three roles. |
| [create-security-policy](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/create-security-policy) | Three progressively mature approaches (inline creds, variable files, Vault) for pushing pre-rules to a Panorama device group. |
| [create-dhcp-reservation](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/create-dhcp-reservation) | Two approaches (panos collection vs. `uri` module) for pushing DHCP server reservations into a Panorama template via XML API. |
| [disable-sip-alg](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/disable-sip-alg) | Uses `panos_config_element` with XPath to disable SIP ALG on all inventory firewalls simultaneously. |
| [override-captive-portal](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/override-captive-portal) | Role-based approach with two task variants (SSH `cli_config` and XML API `uri`) to disable the captive portal. |

### Networking

| Project | Description |
|---------|-------------|
| [create-ipsec-vpn](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/create-ipsec-vpn) | Provisions a complete site-to-site IPsec VPN between two firewalls using five roles for tags, addresses, interfaces, IKE/IPsec profiles, and static routes. |
| [get-interfaces](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/get-interfaces) | Retrieves interface information via `panos_op`, parses XML with `xmltodict`, and displays results. |

### Operations & Monitoring

| Project | Description |
|---------|-------------|
| [show-logs](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/show-logs) | Queries the PAN-OS XML API for dropped traffic logs asynchronously, polls for completion, and displays results in YAML. |
| [export-rules](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/export-rules) | Retrieves security rules from Panorama and exports them to CSV via a Jinja2 template for auditing. |

### Security & Certificates

| Project | Description |
|---------|-------------|
| [tls-decryption-remediation](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/tls-decryption-remediation) | Exports TLS decryption certificates from PAN-OS and deploys them to RHEL and Windows endpoint trust stores. |
| [event-driven](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/panos/event-driven) | EDA rulebooks that listen for PAN-OS log events on port 5000 and trigger remediation playbooks via AAP. |

## Collection Used

All playbooks use the [`paloaltonetworks.panos`](https://galaxy.ansible.com/ui/repo/published/paloaltonetworks/panos/) Ansible collection, which wraps the PAN-OS XML API and provides modules like `panos_security_rule`, `panos_op`, `panos_config_element`, and more.
