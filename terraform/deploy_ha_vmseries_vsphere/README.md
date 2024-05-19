# Deploy VM-Series on vSphere

## Prepare

Rename the example files by stripping off their `.example` extension, and update the contents of these files to reflect your environment.

## Workflow

Initialize the providers

```bash
terraform init
```

Create a workspace and deploy fw1

```bash
terraform workspace new fw1
terraform plan --var-file shared.tfvars --var-file fw1.tfvars
```

Create a workspace and deploy fw2

```bash
terraform workspace new fw2
terraform plan --var-file shared.tfvars --var-file fw2.tfvars
```
