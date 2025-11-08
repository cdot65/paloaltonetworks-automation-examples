# PAN-OS LangGraph Agent

AI agent for automating Palo Alto Networks PAN-OS firewalls using natural language.
Built with LangGraph and pan-os-python.

## Overview

This project demonstrates two approaches to AI-driven network automation:

| Mode | Description | Use Case |
|------|-------------|----------|
| **Autonomous** | ReAct agent with full tool access | Exploratory automation, ad-hoc tasks, |
|                 |                                 | natural language queries |
| **Deterministic** | Step-by-step workflows with conditional routing | Production workflows, |
|                    |                                                 | repeatable processes, |
|                    |                                                 | Ansible-like execution |

### Key Features

- 🤖 **Dual-mode operation**: Autonomous (ReAct) and Deterministic (workflow-based)
- 🔧 **Comprehensive PAN-OS support**: 33 tools across addresses, services, policies, NAT
- 🎯 **LangGraph Studio integration**: Visual debugging and execution
- 🔄 **Retry logic**: Exponential backoff for transient failures
- 🏗️ **Composable subgraphs**: CRUD and commit workflows
- 📝 **Firewall commits**: Job polling with approval gates

## Quickstart

### 1. Prerequisites

- Python 3.11+ (managed via pyenv)
- uv package manager
- PAN-OS firewall (tested on 10.x+)
- Anthropic API key

### 2. Setup

```bash

# Install Python 3.11
pyenv install 3.11
pyenv local 3.11

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your credentials

```bash

### 3. Environment Variables

```bash

# Required
PANOS_HOSTNAME=192.168.1.1
PANOS_USERNAME=admin
PANOS_PASSWORD=your_password
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional
DEFAULT_MODE=autonomous
LOG_LEVEL=INFO

```text

### 4. Run with LangGraph Studio

```bash

# Start LangGraph Studio
langgraph dev

# Or via CLI command (once implemented)
panos-agent studio

```text

Then open `<http://localhost:8000`> and select a graph (autonomous or deterministic).

### 5. CLI Usage

```bash

# Autonomous mode (natural language)
panos-agent run -m autonomous -p "Create address object web-server at 10.1.1.100"
panos-agent run -m autonomous -p "List all service groups"

# Deterministic mode (predefined workflows)
panos-agent list-workflows  # Show all available workflows
panos-agent run -m deterministic -p "simple_address"
panos-agent run -m deterministic -p "web_server_setup"
panos-agent run -m deterministic -p "security_rule_complete"

# Test connection
panos-agent test-connection

# Version info
panos-agent version

```text

## Testing the Graphs

### Autonomous Mode Examples

Test the autonomous ReAct agent with natural language queries:

```bash

# List operations
panos-agent run -p "List all address objects" -m autonomous --log-level ERROR

# Create operations
panos-agent run -p "Create an address object named test-server-123 with IP 192.168.100.123" \\
  -m autonomous --log-level ERROR

# Delete operations
panos-agent run -p "Delete the address object named test-server-123" -m autonomous --log-level ERROR

# Complex queries
panos-agent run -p "Show me all NAT policies and explain what they do" \\
  -m autonomous --log-level ERROR

```bash

**Expected Output (List Example):**

```bash

PAN-OS Agent - Mode: autonomous
Prompt: List all address objects

Response:
Great! There are **37 address objects** currently configured on the PAN-OS
firewall.

Would you like me to:

- Get details about a specific address object?
- Filter or search for particular addresses?
- Create new address objects?
- Modify or delete existing ones?

Let me know how I can help!

Thread ID: 49d5513e-2763-4b54-bdfc-3b6f072d6020

```bash

### Deterministic Mode Examples

Test predefined workflows with step-by-step execution:

```bash

# List available workflows
panos-agent list-workflows

# Simple address creation workflow (2 steps)
panos-agent run -p "simple_address" -m deterministic

# Web server setup workflow (multi-object creation)
panos-agent run -p "web_server_setup" -m deterministic

# Workflow with approval gate
panos-agent run -p "address_with_approval" -m deterministic

```bash

**Expected Output (simple_address):**

```bash

PAN-OS Agent - Mode: deterministic
Prompt: simple_address

[14:08:32] INFO     Loading workflow: simple_address
           INFO     Executing step 1/2: Create address object
           INFO     Validating create for address
           INFO     Checking existence of address: demo-server
           INFO     Connected to PAN-OS 11.1.4-h7 (serial: 021201109830)
           INFO     Object exists: False
           INFO     Creating address: demo-server
           INFO     Successfully created address: demo-server
           INFO     Step evaluation: continue - Address object successfully created
           INFO     Executing step 2/2: Verify address object
           INFO     Validating read for address
           INFO     Reading address: demo-server

Response:
📊 Workflow 'simple_address' Execution Summary

Steps: 2/2
✅ Successful: 2
❌ Failed: 0

Step Details:

  1. ✅ Create address object

  2. ✅ Verify address object

Final Decision: continue
Reason: Address object successfully retrieved (demo-server). No errors reported.
Step completed as expected.

Thread ID: ac43a662-137c-464c-b118-c6d399a7fbe4

```bash

### Testing with Thread IDs

Both modes support conversation continuity using thread IDs:

```bash

# Start a conversation
panos-agent run -p "List address objects" -m autonomous --thread-id my-session-1

# Continue the same conversation
panos-agent run -p "Now create one called test-server at 10.1.1.1" -m autonomous --thread-id
  my-session-1

# Start a fresh conversation
panos-agent run -p "List address objects" -m autonomous --thread-id my-session-2

```bash

### Connection Testing

Always test your connection first before running operations:

```bash

panos-agent test-connection

```bash

**Expected Output:**

```bash

Testing PAN-OS connection...

✅ Connected to PAN-OS 11.1.4-h7 (serial: 021201109830)

```bash

## Architecture

### Project Structure

```bash

panos-agent/
├── src/
│   ├── autonomous_graph.py      # ReAct agent graph
│   ├── deterministic_graph.py   # Workflow graph
│   ├── main.py                  # Graph orchestrator
│   ├── core/
│   │   ├── client.py            # PAN-OS firewall client
│   │   ├── config.py            # Environment config
│   │   ├── state_schemas.py     # All state definitions
│   │   ├── retry_helper.py      # Retry logic
│   │   └── subgraphs/
│   │       ├── crud.py          # Single object operations
│   │       ├── batch.py         # Parallel batch operations
│   │       ├── commit.py        # Commit workflow
│   │       └── deterministic.py # Workflow executor
│   ├── tools/
│   │   ├── address_objects.py
│   │   ├── services.py
│   │   ├── security_policies.py
│   │   ├── nat_policies.py
│   │   └── orchestration/
│   │       ├── crud_operations.py
│   │       └── batch_operations.py
│   └── cli/
│       └── commands.py
├── tests/
├── docs/
│   └── ARCHITECTURE.md
├── langgraph.json               # LangGraph Studio config
├── pyproject.toml
└── README.md

```bash

### Autonomous Mode

ReAct pattern: **agent → tools → agent** loop.

```mermaid

graph LR
    A[User Input] --> B[Agent LLM]
    B --> C{Tool Call?}
    C -->|Yes| D[Execute Tools]
    D --> B
    C -->|No| E[Final Response]

```bash

**Use cases:**

- "Show me all address objects"
- "Create security rule allowing web traffic from Trust to Untrust"
- "Find unused address groups and delete them"

### Deterministic Mode

Step-by-step workflow with conditional routing.

```mermaid

graph TD
    A[Load Workflow] --> B[Execute Step]
    B --> C{LLM Evaluates Result}
    C -->|Success| D{More Steps?}
    C -->|Failure| E[Error Handling]
    D -->|Yes| B
    D -->|No| F[Complete]
    E --> D

```bash

**Use cases:**

- Pre-defined security rule creation workflow
- Multi-step object provisioning
- Repeatable, auditable operations

**Key features:**

- **LLM-based conditional routing**: Agent evaluates each step result
- **HITL approval gates**: Human approval required at critical points
- **Sequential execution**: Predictable, step-by-step workflow
- **Error handling**: Stops on critical errors with detailed reporting

**Available workflows** (6 total):

- `simple_address`: Create and verify single address object
- `address_with_approval`: Address creation with approval gate
- `web_server_setup`: Multi-object creation (addresses, services, groups)
- `multi_address_creation`: Multiple addresses with grouping
- `network_segmentation`: Complete network segment setup
- `complete_security_workflow`: Full workflow with object creation + policy + commit

## Development Status

### ✅ Phase 1: Foundation (Completed)

- [x] Python/uv setup
- [x] Project structure
- [x] Core modules (config, client, state_schemas, retry_helper)
- [x] LangGraph Studio configuration

### ✅ Phase 2: Tools & Subgraphs (Completed)

- [x] PAN-OS tools (22 tools: addresses, services, groups)
- [x] CRUD subgraph
- [x] Orchestration tools (crud_operation)

### ✅ Phase 3: Dual-Mode Graphs (Completed)

- [x] Autonomous graph implementation (ReAct agent)
- [x] Deterministic graph implementation (workflow executor)
- [x] CLI commands (run, list-workflows, test-connection, studio)
- [x] 6 basic workflows with approval gates

### ✅ Phase 4: Advanced Features (Completed)

- [x] **Commit subgraph**: PAN-OS commit with job polling and approval gates
- [x] **Expanded policy tools**: Security policy full CRUD (5 tools)
- [x] **NAT policy tools**: Basic NAT CRUD (4 tools)
- [x] **Orchestration tools**: crud_operation, commit_changes
- [x] **Total: 33 tools** across all categories

### ✅ Phase 5: Testing & Polish (Completed)

- [x] **Pre-commit hooks**: black, flake8, isort auto-formatting
- [x] **Pytest configuration**: Test framework setup with fixtures
- [x] **Mock fixtures**: Firewall, objects, sample data
- [x] **ARCHITECTURE.md**: Comprehensive technical guide
- [x] **SETUP.md**: Development environment guide
- [x] **Code quality**: Linting and formatting standards

## Documentation

### 📚 For Developers

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Complete technical architecture guide
  - **ReAct vs Deterministic comparison**: Detailed workflows, structures, decision-making
  - State management patterns
  - Subgraph design (CRUD, Commit, Deterministic)
  - Testing strategy
  - Troubleshooting guide

- **[SETUP.md](docs/SETUP.md)**: Development environment setup
  - Installation steps
  - IDE configuration
  - Development workflow
  - Pre-commit hooks
  - Common issues

### 🎓 For Users

- **README.md** (this file): Overview and quickstart
- **Workflows**: See `panos-agent list-workflows`
- **LangGraph Studio**: Run `langgraph dev` for visual interface

## Contributing

This is a standalone example project within the broader `paloaltonetworks-automation-examples`
  repository.

## License

See repository root for license information.

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [pan-os-python Documentation](https://pan-os-python.readthedocs.io/)
- [PAN-OS XML API Reference](https://docs.paloaltonetworks.com/pan-os/11-0/pan-os-panorama-api)

---

**Status**: ✅ Complete (All 5 phases + Phase 1 observability)
**Features**: 33 tools, commit workflow, 6 workflows, LangSmith observability, comprehensive docs
**Coverage**: Architecture guide, setup guide, testing examples
**Recent Updates**:

- ✅ LangSmith environment variables and anonymizers (Phase 1.1-1.2)
- ✅ Metadata and tags for observability (Phase 1.3)
- ✅ Fixed CRUD subgraph pan-os-python API usage
- ✅ Fixed deterministic workflow step accumulation bug

**Last Updated**: 2025-01-08
