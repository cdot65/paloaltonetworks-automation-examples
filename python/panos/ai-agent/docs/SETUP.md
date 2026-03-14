# Development Setup Guide

Complete guide for setting up the PAN-OS LangGraph Agent development environment.

## Prerequisites

- **Python 3.11+** (installed via pyenv)
- **uv** package manager
- **PAN-OS firewall** (hardware, VM, or demo instance)
- **Anthropic API key**
- **Git**

## Step-by-Step Setup

### 1. Python Version Management

```bash

# Install pyenv (if not already installed)
# macOS
brew install pyenv

# Linux
curl <<https://pyenv.run>> | bash

# Install Python 3.11
pyenv install 3.11.7
pyenv local 3.11.7
python --version  # Should show 3.11.x

```python

### 2. Install uv Package Manager

```bash

# macOS/Linux
curl -LsSf <<https://astral.sh/uv/install.sh>> | sh

# Or via pip
pip install uv

```text

### 3. Clone and Setup Project

```bash

# Navigate to project directory
cd python/ai-agent-panos

# Create virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies (production)
uv pip install -e .

# Install dev dependencies
uv pip install -e ".[dev]"

```text

### 4. Configure Environment

```bash

# Copy example env file
cp .env.example .env

# Edit with your credentials
# Required variables:
# - PANOS_HOSTNAME
# - PANOS_USERNAME
# - PANOS_PASSWORD
# - ANTHROPIC_API_KEY

```text

### 5. Install Pre-Commit Hooks

```bash

# Install hooks
pre-commit install

# Test hooks (optional)
pre-commit run --all-files

```text

### 6. Verify Installation

```bash

# Test PAN-OS connection
python -m src.cli.commands test-connection

# Run tests
pytest

# List available workflows
python -m src.cli.commands list-workflows

```bash

## Development Workflow

### Running the Agent

**Autonomous Mode:**

```bash

panos-agent run -m autonomous -p "List all address objects"

```text

**Deterministic Mode:**

```bash

panos-agent run -m deterministic -p "simple_address"

```text

**LangGraph Studio:**

```bash

langgraph dev
# Open <<http://localhost:8000>>

```text

### Code Quality

**Format Code:**

```bash

black src/ tests/
isort src/ tests/

```text

**Lint Code:**

```bash

flake8 src/ tests/

```text

**Type Check:**

```bash

mypy src/

```text

**Run All Checks:**

```bash

pre-commit run --all-files

```text

### Testing

**Run All Tests:**

```bash

pytest

```text

**Run Specific Test:**

```bash

pytest tests/test_dependency_resolver.py

```text

**Run with Coverage:**

```bash

pytest --cov=src --cov-report=html
open htmlcov/index.html

```text

**Watch Mode (requires pytest-watch):**

```bash

ptw  # Re-runs tests on file changes

```text

### Adding New Tools

1. Create tool function in appropriate file (e.g., `src/tools/address_objects.py`)

2. Add to tool export list

3. Update `src/tools/__init__.py` to include new tool

4. Write tests in `tests/test_tools.py`

5. Update documentation

**Template:**

```python

from langchain_core.tools import tool

@tool
def my_new_tool(param: str) -> str:
    """Tool description with examples.

    Args:
        param: Parameter description

    Returns:
        Success/failure message

    Example:
        my_new_tool(param="value")
    """
    try:
        # Implementation
        return "✅ Success message"
    except Exception as e:
        return f"❌ Error: {e}"

```text

### Adding New Workflows

1. Edit `src/workflows/definitions.py`

2. Add workflow to `WORKFLOWS` dict

3. Test with `panos-agent run -m deterministic -p "workflow_name"`

**Template:**

```python

"my_workflow": {
    "name": "My Workflow Name",
    "description": "What this workflow does",
    "steps": [
        {
            "name": "Step 1 name",
            "type": "tool_call",
            "tool": "address_create",
            "params": {"name": "obj-1", "value": "10.1.1.1"},
        },
        {
            "name": "Approval gate",
            "type": "approval",
            "message": "Approve to continue?",
        },
    ],
},

```text

## Troubleshooting

### Issue: uv command not found

**Solution:**

```bash

# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.cargo/bin:$PATH"
source ~/.bashrc

```bash

### Issue: Python version mismatch

**Solution:**

```bash

pyenv local 3.11.7
python --version  # Verify

```python

### Issue: PAN-OS connection fails

**Solution:**
1. Check firewall reachability: `ping $PANOS_HOSTNAME`

2. Verify credentials

3. Check firewall management interface enabled

4. Test with pan-os-python directly:

```python

from panos.firewall import Firewall
fw = Firewall("192.168.1.1", api_username="admin", api_password="password")
fw.refresh_system_info()
print(fw.version)

```text

### Issue: Anthropic API errors

**Solution:**
1. Verify API key: `echo $ANTHROPIC_API_KEY`

2. Check API quota/limits

3. Test with simple call:

```python

from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
print(llm.invoke("Hello"))

```text

### Issue: Pre-commit hooks failing

**Solution:**

```bash

# Fix automatically
black src/ tests/
isort src/ tests/

# Skip hooks (not recommended)
git commit --no-verify

```text

## IDE Setup

### VS Code

**Recommended Extensions:**
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Black Formatter (ms-python.black-formatter)
- isort (ms-python.isort)

**Settings (.vscode/settings.json):**

```json

{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}

```text

### PyCharm

1.
Set interpreter: Settings → Project → Python Interpreter → Add → Virtualenv → Existing →
  `.venv/bin/python`

2. Enable Black: Settings → Tools → Black → Enable

3. Configure flake8: Settings → Tools → External Tools → Add flake8

## Next Steps

1. Read [ARCHITECTURE.md](./ARCHITECTURE.md) for technical details

2. Browse [workflows/definitions.py](../src/workflows/definitions.py) for examples

3. Run `langgraph dev` to explore in LangGraph Studio

4. Try autonomous mode with natural language prompts

5. Create custom workflows for your use cases

## Resources

- **LangGraph**: <<https://langchain-ai.github.io/langgraph/>>
- **pan-os-python**: <<https://pan-os-python.readthedocs.io/>>
- **PAN-OS API**: <<https://docs.paloaltonetworks.com/pan-os/11-0/pan-os-panorama-api>>
- **Anthropic**: <<https://docs.anthropic.com/>>

---

**Questions?** Open an issue or check main README.md
