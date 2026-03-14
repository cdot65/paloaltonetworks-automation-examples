# Python Examples

26 Python projects for automating PAN-OS firewalls, Panorama, Prisma AIRS AI security, and general network operations.

## Project Categories

| Category | Count | Description |
|----------|-------|-------------|
| [PAN-OS Tools](panos.md) | 11 | Firewall configuration, AI agent, certificate management, BGP, upgrades |
| [Panorama Tools](panorama.md) | 7 | Address objects, interfaces, settings, log retrieval, sync reports |
| [Prisma AIRS](prisma-airs.md) | 4 | AI security scanning, MCP server, batch analysis, stress testing |
| [General Utilities](general.md) | 4 | Certificate chains, Django starter, ThreatVault lookup |

## Common Prerequisites

- Python 3.11+ (some projects require 3.12+)
- Virtual environment (`python3 -m venv .venv`)
- PAN-OS firewall, Panorama, or AIRS API access

## Key Libraries

| Library | Used For |
|---------|----------|
| `pan-os-python` | PAN-OS SDK for firewall/Panorama management |
| `panos-upgrade-assurance` | Pre/post-upgrade health checks and snapshots |
| `pan-aisecurity` | Prisma AIRS API integration |
| `langgraph` | AI agent orchestration (ai-agent project) |
| `dynaconf` | Hierarchical YAML configuration |
| `pydantic` | Data validation and settings management |
| `httpx` | Async HTTP client |

## Configuration Pattern

Most Python projects use `.env` files for credentials:

```bash
cp .env.example .env
# Edit .env with your device details
```

!!! tip "Dependency Management"
    Projects use `pip` with `requirements.txt`, `poetry`, or `uv` depending on complexity. Check each project's README for the exact install command.
