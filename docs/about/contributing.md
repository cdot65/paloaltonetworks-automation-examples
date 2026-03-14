# Contributing

## Adding a New Example

1. Create a directory following the `{technology}/{target-platform}/{project-name}` convention
2. Include a README following the [standardized template](../getting-started/structure.md) for your technology
3. Use placeholder credentials (`your-api-key-here`, `192.168.1.1`) -- never real secrets
4. Add a `.env.example` or `terraform.tfvars.example` for configuration
5. Ensure your project is self-contained with its own dependencies

## Code Style

| Technology | Formatter | Linter |
|------------|-----------|--------|
| Python | Black (100 char line) | ruff, flake8 |
| Terraform | `terraform fmt` | `terraform validate` |
| Go | `gofmt` | `go vet` |
| YAML | 2-space indent | yamllint |

## README Standards

Each technology has a standardized README template ensuring consistent documentation:

- **Quickstart** with exact commands from zero to running
- **Configuration** with variable tables and security notes
- **Usage** with expected output blocks
- **Troubleshooting** with common issues table

## Security

- Never commit real API keys, passwords, or internal hostnames
- All `.env`, `terraform.tfvars`, and `.secrets.yaml` files are git-ignored
- Use Ansible Vault for sensitive variable files
- Use `withCredentials` in Jenkins pipelines
