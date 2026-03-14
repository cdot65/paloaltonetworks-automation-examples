# PAN-OS AI Agent for Firewall Automation

## Overview

This project provides a LangGraph-based AI agent for automating Palo Alto Networks PAN-OS firewall configuration through natural language or predefined workflows. It supports two execution modes: an autonomous ReAct agent that interprets natural language prompts and decides which tools to call via Anthropic Claude, and a deterministic mode that executes predefined step-by-step workflows with optional human approval gates. Built with LangGraph, LangChain, pan-os-python, Pydantic, and Typer, the agent manages address objects, address groups, services, service groups, security policies, NAT policies, and commits. State is persisted to a SQLite checkpointer for conversation continuity and resumability.

## Prerequisites

- Python 3.11+
- Network access to a PAN-OS firewall (NGFW or VM-Series) with API enabled
- PAN-OS admin credentials (username/password or API key)
- Anthropic API key for Claude LLM access
- (Optional) LangSmith API key for tracing and observability

## Quickstart

1. Clone the repository and navigate to the project directory:

    ```bash
    cd python/panos/ai-agent
    ```

2. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    ```

    > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python and other projects. This prevents version conflicts and ensures reproducibility.

3. Install dependencies:

    ```bash
    pip install -e .
    ```

    For development dependencies (linting, testing, pre-commit hooks):

    ```bash
    pip install -e ".[dev]"
    ```

4. Copy `.env.example` to `.env` and populate with your values:

    ```bash
    cp .env.example .env
    ```

5. Run the agent:

    ```bash
    panos-agent run -p "List all address objects" -m autonomous
    ```

## Configuration

Create a `.env` file in the project root (see `.env.example`):

```dotenv
PANOS_HOSTNAME=192.168.1.1
PANOS_USERNAME=admin
PANOS_PASSWORD=your_password_here
ANTHROPIC_API_KEY=sk-ant-your-key-here
LANGSMITH_API_KEY=lsv2_your_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=panos-agent
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
DEFAULT_MODE=autonomous
LOG_LEVEL=INFO
```

| Variable | Required | Description |
|---|---|---|
| `PANOS_HOSTNAME` | Yes | IP or hostname of the PAN-OS firewall |
| `PANOS_USERNAME` | Yes | Admin username for firewall authentication |
| `PANOS_PASSWORD` | Yes | Admin password for firewall authentication |
| `PANOS_API_KEY` | No | API key (alternative to username/password) |
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude LLM |
| `LANGSMITH_API_KEY` | No | LangSmith API key for tracing |
| `LANGSMITH_TRACING` | No | Enable LangSmith tracing (default: false) |
| `LANGSMITH_PROJECT` | No | LangSmith project name (default: panos-agent) |
| `LANGSMITH_ENDPOINT` | No | LangSmith API endpoint |
| `DEFAULT_MODE` | No | Default agent mode: autonomous or deterministic |
| `LOG_LEVEL` | No | Logging level: DEBUG, INFO, WARNING, ERROR |

**Security note:** Never commit your `.env` file to version control. It is already listed in `.gitignore`.

## Usage

### Autonomous Mode

Natural language prompts interpreted by the LLM agent:

```bash
panos-agent run -p "List all address objects" -m autonomous
panos-agent run -p "Create address object web-server at 10.1.1.100"
```

### Deterministic Mode

Execute predefined workflows:

```bash
panos-agent run -p "simple_address" -m deterministic
panos-agent run -p "web_server_setup" -m deterministic
panos-agent run -p "complete_security_workflow" -m deterministic
```

### Other Commands

```bash
panos-agent list-workflows              # List available deterministic workflows
panos-agent test-connection             # Test firewall connectivity
panos-agent studio                      # Launch LangGraph Studio for visual debugging
panos-agent version                     # Show agent version
panos-agent checkpoints list            # List checkpoint threads
panos-agent checkpoints show <id>       # Show checkpoint details
panos-agent checkpoints history <id>    # Show checkpoint history
panos-agent checkpoints delete <id>     # Delete checkpoints for a thread
panos-agent checkpoints prune --days 30 # Prune checkpoints older than 30 days
```

### CLI Flags

| Flag | Short | Description |
|---|---|---|
| `--prompt` | `-p` | User prompt or workflow name |
| `--mode` | `-m` | Agent mode: autonomous or deterministic (default: autonomous) |
| `--thread-id` | `-t` | Thread ID for conversation continuity |
| `--log-level` | `-l` | Logging level (default: INFO) |

### Expected Output

Autonomous mode:

```
PAN-OS Agent - Mode: autonomous
Prompt: List all address objects

Response:
Here are the current address objects on the firewall:

- web-server-1: 10.10.1.100 (Web server primary)
- db-server-1: 10.20.1.10 (Database server 1)
- dmz-subnet: 10.100.0.0/24 (DMZ network segment)

Thread ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

Deterministic mode:

```
PAN-OS Agent - Mode: deterministic
Prompt: simple_address

Response:
Workflow 'Simple Address Creation' completed successfully.

Step 1: Create address object - SUCCESS
  Created address object 'demo-server' with value 10.1.1.100

Step 2: Verify address object - SUCCESS
  Verified address object 'demo-server' exists

Thread ID: f9e8d7c6-b5a4-3210-fedc-ba0987654321
```

The response content depends on the prompt and the current firewall state. In autonomous mode the LLM decides which tools to call and formats the response. In deterministic mode the workflow steps execute sequentially and a summary is returned.

## Project Structure

```
ai-agent/
├── .env.example                     # Environment variable template
├── pyproject.toml                   # Project metadata and dependencies (hatchling)
├── langgraph.json                   # LangGraph Studio graph registry
├── src/
│   ├── __init__.py
│   ├── autonomous_graph.py          # ReAct agent graph (agent -> tools loop)
│   ├── deterministic_graph.py       # Workflow execution graph (load -> execute)
│   ├── cli/
│   │   ├── commands.py              # Typer CLI entry point (run, studio, test-connection, etc.)
│   │   └── checkpoint_commands.py   # Checkpoint management subcommands
│   ├── core/
│   │   ├── config.py                # Pydantic-settings from .env, timeout constants
│   │   ├── client.py                # PAN-OS firewall client singleton (pan-os-python)
│   │   ├── state_schemas.py         # LangGraph TypedDict state definitions
│   │   ├── checkpoint_manager.py    # SQLite checkpointer singleton
│   │   ├── retry_helper.py          # Retry logic utilities
│   │   ├── retry_policies.py        # Retry policy configuration
│   │   ├── anonymizers.py           # Data anonymization for logs
│   │   └── subgraphs/              # Reusable subgraphs (commit, crud, deterministic)
│   ├── tools/
│   │   ├── __init__.py              # ALL_TOOLS aggregation (31 tools)
│   │   ├── address_objects.py       # Address CRUD (5 tools)
│   │   ├── address_groups.py        # Address group CRUD (5 tools)
│   │   ├── services.py              # Service CRUD (5 tools)
│   │   ├── service_groups.py        # Service group CRUD (5 tools)
│   │   ├── security_policies.py     # Security policy CRUD (5 tools)
│   │   ├── nat_policies.py          # NAT policy CRUD (4 tools)
│   │   └── orchestration/           # Unified CRUD and commit workflow tools
│   └── workflows/
│       └── definitions.py           # 7 predefined workflow playbooks
├── tests/                           # Test suite (pytest)
└── docs/                            # Documentation
```

## Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| Connection refused | Firewall unreachable or wrong hostname | Verify `PANOS_HOSTNAME` and network connectivity; run `panos-agent test-connection` |
| Invalid credentials | Wrong username or password | Check `PANOS_USERNAME` and `PANOS_PASSWORD` in `.env` |
| `ModuleNotFoundError: No module named 'langgraph'` | Dependencies not installed | Run `pip install -e .` inside the activated virtual environment |
| SSL certificate verification failed | Self-signed cert on firewall | pan-os-python disables SSL verification by default; ensure no proxy interferes |
| Timeout error during graph execution | LLM or firewall response too slow | Autonomous mode has a 300s timeout, deterministic 600s; reduce prompt complexity or check firewall responsiveness |
| `ANTHROPIC_API_KEY` not set | Missing API key in environment | Add `ANTHROPIC_API_KEY` to your `.env` file |
| Workflow not found in deterministic mode | Invalid workflow name | Run `panos-agent list-workflows` to see available workflows |
| Checkpoint database locked | Concurrent access to SQLite | Ensure only one agent instance runs at a time |
