# PAN-OS Python Tools

11 Python projects for automating PAN-OS firewalls, from configuration management to an AI-powered automation agent.

## Projects

### AI & Automation

| Project | Description |
|---------|-------------|
| [ai-agent](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/ai-agent) | LangGraph-based AI agent with autonomous (Claude LLM + ReAct) and deterministic workflow modes for managing address objects, services, security/NAT policies, and commits via natural language. |

### Configuration

| Project | Description |
|---------|-------------|
| [configure-security-policies](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/configure-security-policies) | Reads hierarchical YAML configs for device groups, tags, addresses, services, and rules, then pushes to Panorama using Dynaconf and `pan-os-python`. |
| [configure-bgp-peer](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/configure-bgp-peer) | Configures BGP peering with virtual router, eBGP peer group, and peers from a YAML settings file. |
| [configure-static-dns](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/configure-static-dns) | Reads DNS proxy static entries from YAML, diffs against current state, and creates/updates only changed entries. |
| [admin-password](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/admin-password) | Rotates admin passwords with optional cryptographically secure random generation and interactive confirmation. |

### Operations

| Project | Description |
|---------|-------------|
| [global-search](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/global-search) | Retrieves merged running+candidate config, walks the XML tree for keyword matches, and renders results with XPath and YAML detail. |
| [nat64-counters](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/nat64-counters) | Queries global counters and filters for NAT64/NPTv6 entries, displaying name, value, rate, and severity using `httpx` and `lxml`. |
| [block-gp-logins](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/block-gp-logins) | Queries failed GlobalProtect auth attempts, extracts source IPs, and registers them as DAG tag entries for automated blocking. |

### Upgrades & Certificates

| Project | Description |
|---------|-------------|
| [upgrade-assurance](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/upgrade-assurance) | Three scripts demonstrating readiness checks, health checks, and pre/post-upgrade snapshot comparison using `panos-upgrade-assurance`. |
| [upgrade](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/upgrade) | Pointer to the external `pan-os-upgrade` CLI for automated backups, readiness checks, and OS upgrades. |
| [acme-certificate-push](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/panos/acme-certificate-push) | Distributes Let's Encrypt certificates to multiple firewalls using the `acme.sh` PAN-OS deploy hook. |
