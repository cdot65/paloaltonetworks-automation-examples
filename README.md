# Palo Alto Networks Automation Examples

A curated collection of 67+ automation examples for Palo Alto Networks products, spanning five technologies and covering real-world use cases from firewall configuration to AI-powered security scanning.

> For detailed walkthroughs, architecture guides, and per-project documentation, visit the [GitHub Pages site](https://cdot65.github.io/paloaltonetworks-automation-examples/) *(coming soon)*.

## What's Inside

| Technology | Projects | What You'll Find |
|------------|----------|------------------|
| **Ansible** | 27 | Playbooks for PAN-OS, Panorama, vCenter, event-driven automation, and custom execution environments |
| **Python** | 26 | CLI tools, API integrations, AI agents (LangGraph), MCP servers, upgrade workflows |
| **Terraform** | 8 | Infrastructure-as-code for PAN-OS, Strata Cloud Manager, GCP VM-Series, vCenter |
| **Go** | 6 | High-performance CLI tools for counters, commits, session analysis, WildFire |
| **Jenkins** | 4 | CI/CD pipelines, Kubernetes agents, Helm charts for Jenkins-on-K8s |

## Products Covered

- **PAN-OS** -- Firewall configuration, security policies, NAT, IPsec, BGP, upgrades, log analysis
- **Panorama** -- Centralized management, device groups, content updates, dynamic inventory
- **Strata Cloud Manager (SCM)** -- Address objects, security rules, EDLs via Terraform modules
- **Prisma AIRS** -- AI runtime security scanning, batch analysis, MCP server integration
- **GCP / vCenter** -- VM-Series deployment and lifecycle management

## Repository Structure

```
.
├── ansible/
│   ├── event-driven-ansible/    # EDA container images
│   ├── execution-environments/  # Custom EE images
│   ├── panos/                   # PAN-OS playbooks
│   ├── panorama/                # Panorama playbooks
│   └── vcenter/                 # VM-Series deployment
├── go/
│   ├── panos/                   # PAN-OS CLI tools
│   └── panorama/                # Panorama CLI tools
├── jenkins/
│   ├── docker/                  # Agent images
│   ├── helm/                    # Jenkins Helm chart
│   ├── manifests/               # K8s RBAC & resources
│   └── pipelines/               # Groovy pipeline scripts
├── python/
│   ├── general/                 # Utilities & web frameworks
│   ├── panos/                   # PAN-OS automation & AI agent
│   ├── panorama/                # Panorama tools
│   └── prisma-airs/             # AI Security integrations
└── terraform/
    ├── gcp/                     # GCP VM-Series
    ├── panos/                   # PAN-OS provider examples
    ├── scm/                     # Strata Cloud Manager modules
    └── vcenter/                 # vSphere deployment
```

Each project is self-contained with its own README, dependencies, and configuration.

## Getting Started

1. Browse the directory for your technology and product of interest
2. Read the project's README for prerequisites, setup, and usage
3. Copy the example config files (`.env.example`, `terraform.tfvars.example`, etc.) and fill in your values

Every project follows a standardized README format with quickstart instructions, configuration tables, expected output, and troubleshooting guides.

## Documentation

Full documentation is published via GitHub Pages using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), including:

- Per-project walkthroughs and architecture overviews
- Getting started guides for each technology
- Configuration reference and examples

Visit: [cdot65.github.io/paloaltonetworks-automation-examples](https://cdot65.github.io/paloaltonetworks-automation-examples/) *(coming soon)*

## License

MIT
