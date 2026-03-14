# Configure Site-to-Site IPsec VPN on PAN-OS Firewalls

## Overview

This project provisions a complete site-to-site IPsec VPN between two Palo Alto Networks firewalls using the `paloaltonetworks.panos` Ansible collection. Five roles execute in sequence: `create_tags` defines color-coded object tags, `create_address_objects` creates shared and per-site address objects, `create_interfaces` configures ethernet and tunnel interfaces, `configure_vpn` sets up IKE crypto profiles, IKE gateways, IPsec crypto profiles, and IPsec tunnels, and `configure_static_routes` adds default routes. Shared configuration lives in `group_vars/all/` while site-specific settings (peer IPs, tunnel endpoints, IKE gateways) are defined per-host in `host_vars/`.

## Prerequisites

- Python 3.8+
- Ansible Core 2.10+
- `paloaltonetworks.panos` Ansible collection
- `pan-os-python` Python library
- Two PAN-OS firewalls with API access enabled
- Firewall admin credentials (username/password)

## Quickstart

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/ansible/panos/create-ipsec-vpn
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Ansible and the PAN-OS Python library:

   ```bash
   pip install ansible pan-os-python
   ```

4. Install the PAN-OS Ansible collection:

   ```bash
   ansible-galaxy collection install paloaltonetworks.panos
   ```

5. Copy the vault example and fill in your credentials:

   ```bash
   cp group_vars/all/vault.yaml.example group_vars/all/vault.yaml
   # Edit vault.yaml with your firewall username and password
   ansible-vault encrypt group_vars/all/vault.yaml
   ```

6. Update `inventory.yaml` with your firewall hostnames and run:

   ```bash
   ansible-playbook playbook.yml --ask-vault-pass
   ```

## Configuration

### Inventory

Edit `inventory.yaml` to list your firewall hostnames:

```yaml
all:
  children:
    firewalls:
      hosts:
        dallas-vfw-01:
          ansible_host: 10.0.1.1
        san-vfw-01:
          ansible_host: 10.0.2.1
```

Each hostname under `firewalls` becomes a target. Set `ansible_host` to the management IP or FQDN if the inventory hostname does not resolve via DNS.

### Credentials

Create `group_vars/all/credentials.yaml` with your firewall admin credentials:

```yaml
username: "your-firewall-admin-username"
password: "your-firewall-admin-password"
```

Encrypt with Ansible Vault:

```bash
ansible-vault encrypt group_vars/all/credentials.yaml
```

The roles reference credentials via a `provider` variable. You may need to define a `provider` dict in group_vars that maps to these credentials.

### Variables

| Variable | Location | Required | Description |
|----------|----------|----------|-------------|
| `username` | `group_vars/all/credentials.yaml` | Yes | Firewall admin username |
| `password` | `group_vars/all/credentials.yaml` | Yes | Firewall admin password |
| `tags` | `group_vars/all/tags.yaml` | Yes | Tag objects with name, color, and comments |
| `shared_address_objects` | `group_vars/all/address_objects.yaml` | Yes | Address objects shared across all firewalls |
| `ethernet_interfaces` | `group_vars/all/interfaces.yaml` | Yes | Ethernet interface definitions (name, mode, IP, zone) |
| `tunnel_interfaces` | `group_vars/all/interfaces.yaml` | Yes | Tunnel interface definitions (name, IP, zone, VR) |
| `crypto_profiles` | `group_vars/all/crypto.yaml` | Yes | IKE crypto profile parameters (DH, auth, encryption) |
| `ipsec_profiles` | `group_vars/all/crypto.yaml` | Yes | IPsec crypto profile parameters |
| `static_routes` | `group_vars/all/static_route.yaml` | Yes | Static route definitions |
| `local_address_objects` | `host_vars/<host>/address_objects.yaml` | Yes | Per-site address objects (WAN, LAN, DMZ, tunnel IPs) |
| `ike_gateways` | `host_vars/<host>/ike_gateways.yaml` | Yes | IKE gateway config (peer IP, PSK, interface, version) |
| `ipsec_tunnels` | `host_vars/<host>/ipsec.yaml` | Yes | IPsec tunnel-to-gateway-to-profile mapping |

## Usage

### Basic Run

Deploy the full VPN configuration to both sites:

```bash
ansible-playbook playbook.yml --ask-vault-pass
```

### Dry Run

```bash
ansible-playbook playbook.yml --check --ask-vault-pass
```

Check mode simulates the playbook run without pushing any configuration to the firewalls. Each PAN-OS module task reports whether it would create or modify an object.

### Variable Override

Deploy to a single site with a different IKE version:

```bash
ansible-playbook playbook.yml --limit dallas-vfw-01 -e "ike_version=ikev1" --ask-vault-pass
```

### Verbose Debugging

```bash
ansible-playbook playbook.yml -vvv --ask-vault-pass
```

### Expected Output

```
PLAY [firewalls] ***************************************************************

TASK [create_tags : Create tags] ***********************************************
changed: [dallas-vfw-01] => (item={'name': 'VPN', 'color': 'red', 'comments': 'All VPN objects'})
changed: [dallas-vfw-01] => (item={'name': 'DMZ', 'color': 'orange', 'comments': 'All DMZ objects'})
changed: [dallas-vfw-01] => (item={'name': 'WAN', 'color': 'purple', 'comments': 'All WAN objects'})
changed: [dallas-vfw-01] => (item={'name': 'LAN', 'color': 'green', 'comments': 'All LAN objects'})
changed: [san-vfw-01] => (item={'name': 'VPN', 'color': 'red', 'comments': 'All VPN objects'})
...

TASK [create_address_objects : Create shared address objects universal to all firewalls] ***
changed: [dallas-vfw-01] => (item={'name': 'Dallas-WAN-IP', ...})
changed: [dallas-vfw-01] => (item={'name': 'SanAntonio-WAN-IP', ...})
...

TASK [create_interfaces : Create ethernet interfaces] **************************
changed: [dallas-vfw-01] => (item={'name': 'ethernet1/1', ...})
...

TASK [configure_vpn : Create IKE crypto profiles] *****************************
changed: [dallas-vfw-01] => (item={'name': 'remote-office-crypto-profile', ...})
...

TASK [configure_vpn : Create IKE gateway config to the firewall] **************
changed: [dallas-vfw-01] => (item={'name': 'SanAntonio-IKE-GW', ...})
...

TASK [configure_vpn : Create IPSec tunnel to IKE gateway profile] *************
changed: [dallas-vfw-01] => (item={'name': 'SanAntonio-VPN', ...})
...

TASK [configure_static_routes : Create static default route] ******************
changed: [dallas-vfw-01] => (item={'name': 'Default Route', ...})
...

PLAY RECAP *********************************************************************
dallas-vfw-01              : ok=8    changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
san-vfw-01                 : ok=8    changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

- `ok=8` -- all eight task groups completed for each firewall.
- `changed=8` -- tags, address objects, interfaces, crypto profiles, gateways, tunnels, and routes were all created.
- `failed=0` -- no errors. If a firewall rejects a configuration, this counter increments.

## Project Structure

```
create-ipsec-vpn/
├── ansible.cfg                              # Ansible settings (inventory, timeouts)
├── inventory.yaml                           # Firewall hosts (dallas, san-antonio)
├── playbook.yml                             # Main playbook importing five roles
├── group_vars/
│   └── all/
│       ├── address_objects.yaml             # Shared address objects (WAN IPs)
│       ├── crypto.yaml                      # IKE and IPsec crypto profile parameters
│       ├── interfaces.yaml                  # Ethernet and tunnel interface definitions
│       ├── python.yaml                      # Python interpreter override
│       ├── static_route.yaml                # Default route definition
│       ├── tags.yaml                        # Tag objects (VPN, DMZ, WAN, LAN)
│       └── vault.yaml.example              # Credential template (copy to vault.yaml)
├── host_vars/
│   ├── dallas-vfw-01/
│   │   ├── address_objects.yaml             # Dallas-specific address objects
│   │   ├── ike_gateways.yaml                # Dallas IKE gateway (peer: SanAntonio)
│   │   └── ipsec.yaml                       # Dallas IPsec tunnel mapping
│   └── san-vfw-01/
│       ├── address_objects.yaml             # San Antonio-specific address objects
│       ├── ike_gateways.yaml                # San Antonio IKE gateway (peer: Dallas)
│       └── ipsec.yaml                       # San Antonio IPsec tunnel mapping
└── roles/
    ├── create_tags/tasks/main.yml           # Create color-coded tag objects
    ├── create_address_objects/tasks/main.yml # Create shared + local address objects
    ├── create_interfaces/tasks/main.yml     # Configure ethernet and tunnel interfaces
    ├── configure_vpn/tasks/main.yml         # IKE crypto, gateways, IPsec profiles, tunnels
    └── configure_static_routes/tasks/main.yml # Static default route
```

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Connection refused to firewall | Firewall management interface unreachable | Verify network connectivity and that HTTPS API is enabled on the firewall |
| Invalid credentials / authentication failure | Wrong username or password in vault | Update `group_vars/all/vault.yaml` and re-encrypt with `ansible-vault encrypt` |
| Module not found: `paloaltonetworks.panos` | Collection not installed | Run `ansible-galaxy collection install paloaltonetworks.panos` |
| Timeout during API calls | Firewall under heavy load or slow link | Increase `timeout` in `ansible.cfg` (currently 240 seconds) |
| Address object already exists with different value | Object created by a previous run with different data | Delete the existing object on the firewall first, or use the module's `state: replaced` if supported |
| Pre-shared key mismatch between sites | Different PSK values in `ike_gateways.yaml` for each host | Ensure both `host_vars/dallas-vfw-01/ike_gateways.yaml` and `host_vars/san-vfw-01/ike_gateways.yaml` use the same `pre_shared_key` |

## Ansible Concepts Used

- **Playbook**: A YAML file defining which roles to apply to which hosts. `playbook.yml` imports five roles against the `firewalls` group.

- **Inventory**: A file listing hosts and groups. Two firewall hosts are defined under the `firewalls` group.

- **Role**: A reusable, self-contained unit of Ansible content. Each of the five roles handles one aspect of VPN setup (tags, addresses, interfaces, VPN config, routing).

- **Module**: A unit of code Ansible executes. This project uses PAN-OS modules: `panos_tag_object`, `panos_address_object`, `panos_interface`, `panos_tunnel`, `panos_ike_crypto_profile`, `panos_ike_gateway`, `panos_ipsec_profile`, `panos_ipsec_tunnel`, and `panos_static_route`.

- **Collection**: A distribution format for Ansible content. `paloaltonetworks.panos` provides all PAN-OS modules used in the roles.

- **Group Vars**: Variable files in `group_vars/all/` that apply to every host. Shared objects like tags, crypto profiles, and interface definitions are defined here.

- **Host Vars**: Variable files in `host_vars/<hostname>/` that apply only to a specific host. Site-specific address objects, IKE gateways, and IPsec tunnels are defined per-firewall.

- **Vault**: Ansible Vault encrypts sensitive files (usernames, passwords, PSKs). The `vault.yaml.example` file provides a template.

- **Check Mode**: A dry-run mode (`--check`) that shows what the playbook would change without making API calls to the firewalls.
