# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Monorepo of Palo Alto Networks automation examples across Python, Go, TypeScript, Bash, Terraform, and Ansible. ~50+ independent projects organized by language/tool.

## Repository Structure

- `python/` — 36+ projects: AI agents (LangGraph), MCP servers, PAN-OS config scripts, Prisma Cloud tools
- `terraform/` — SCM modules, PAN-OS providers, GCP VM-Series deployment
- `ansible/` — Playbooks for PAN-OS, Panorama, vCenter automation
- `go/` — CLI tools for firewall commits, session analysis, counters
- `typescript/saute/` — Angular 15 + Python backend for PAN-OS management
- `containers/` — Docker/Ansible execution environments
- `kubernetes/` — Helm charts for PAN-OS telemetry
- `jenkins/` — CI/CD pipeline examples

Each subdirectory is a self-contained project with its own deps and build system. No shared build across the monorepo.

## Key Active Projects

### python/ai-agent-panos
LangGraph AI agent for PAN-OS automation. Dual-mode: autonomous (ReAct) and deterministic workflows. Uses hatchling build system.

```bash
cd python/ai-agent-panos
pip install -e ".[dev]"

# Run tests
pytest                          # all tests with coverage
pytest tests/unit/              # unit tests only
pytest tests/unit/test_foo.py   # single test file
pytest -k "test_name"           # single test by name

# Code quality
black src/ tests/               # format
isort src/ tests/               # sort imports
ruff check src/                 # lint
flake8 src/                     # lint
```

CLI entry point: `panos-agent` (via `src.cli.commands:app`, Typer-based)

### python/aisecurity-mcp-server
MCP server for AI Security scanning. Uses `uv` package manager, Python 3.12+. See its own `CLAUDE.md` for details.

### terraform/scm
Strata Cloud Manager Terraform modules. Standard `terraform init/validate/fmt/plan/apply` workflow.

## Root-Level Python Environment

```bash
poetry install                  # install deps from root pyproject.toml
poetry add <pkg>                # add dependency
```

Root Poetry env provides: ansible, pan-os-python, pydantic, invoke, pulumi, pandas.

## Code Style

- **Python**: black (line-length=100, py311), isort (black profile), flake8, ruff
- **Root .flake8**: ignores E501, W503; max-line-length=100; excludes tasks.py
- **Terraform**: `terraform fmt`
- **Pre-commit hooks** exist in some subprojects (ai-agent-panos has black, flake8, isort)

## Architecture Notes

### ai-agent-panos (most actively developed)
- `src/autonomous_graph.py` — ReAct agent graph
- `src/deterministic_graph.py` — Workflow executor graph
- `src/core/` — Config (Pydantic settings), PAN-OS client wrapper, state schemas, retry helpers
- `src/core/subgraphs/` — CRUD, commit, batch operation subgraphs
- `src/tools/` — 33 LangChain tools for PAN-OS (address objects, services, security policies, NAT)
- `src/cli/` — Typer CLI
- SQLite-based persistent checkpointing (LangGraph)
- LangSmith observability with automatic anonymization
- `langgraph.json` defines two graphs for LangGraph Studio

### terraform/scm
- `modules/` — Reusable modules (address, group, EDL, rule)
- `environments/` — Dev/prod configs
- `examples/` — Usage examples
