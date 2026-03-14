# Repository Structure

The repository follows a three-level hierarchy: `{technology}/{target-platform}/{project-name}`.

```
.
├── ansible/
│   ├── event-driven-ansible/    # EDA container images
│   ├── execution-environments/  # Custom EE images (panos, nautobot, netbox)
│   ├── panos/                   # 11 PAN-OS playbooks
│   ├── panorama/                # 6 Panorama playbooks
│   └── vcenter/                 # VM-Series deployment
├── go/
│   ├── panos/                   # Commit, session analysis CLI tools
│   └── panorama/                # Mock API server (stub)
├── jenkins/
│   ├── docker/                  # Custom agent image with kubectl
│   ├── helm/                    # Jenkins Helm chart values
│   ├── manifests/               # K8s RBAC for agent pods
│   └── pipelines/               # Groovy pipeline scripts
├── python/
│   ├── general/                 # Certificates, Django, ThreatVault
│   ├── panos/                   # 11 PAN-OS tools + AI agent
│   ├── panorama/                # 7 Panorama tools
│   └── prisma-airs/             # 4 AIRS integrations
└── terraform/
    ├── gcp/                     # VM-Series on GCP
    ├── panos/                   # PAN-OS provider v1 & v2 examples
    ├── scm/                     # Strata Cloud Manager modules
    └── vcenter/                 # Debian VM deployment
```

## Conventions

- Each project is **self-contained** with its own dependencies, config, and README
- READMEs follow **standardized templates** per technology with quickstart, configuration, usage, and troubleshooting sections
- Credentials use **placeholder values** (`your-api-key-here`, `192.168.1.1`) -- never real secrets
- Python projects use **virtual environments** or **uv**
- Terraform projects include **init/plan/apply** workflows with expected output
