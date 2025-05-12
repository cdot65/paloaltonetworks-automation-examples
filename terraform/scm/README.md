# Strata Cloud Manager (SCM) Terraform Automation

This repository provides Terraform modules and examples for provisioning core resources in Palo Alto Networks Strata Cloud Manager (SCM):
- Address Objects
- Address Groups
- External Dynamic Lists (EDL)
- Security Rules

## Structure

- `modules/` — Reusable Terraform modules for SCM resources
- `environments/` — Environment-specific configurations (e.g., dev, prod)
- `examples/` — Usage examples for core modules
- `main.tf`, `variables.tf`, `outputs.tf` — Entry-point for root-level deployments

## Getting Started
1. Clone the repository
2. Review and update variables in `environments/`
3. Use `terraform init`, `plan`, and `apply` as needed

---

Refer to each module's README for detailed usage and input/output variables.
