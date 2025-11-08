# PAN-OS LangGraph Agent - Architecture Documentation

> Comprehensive technical guide for developers working on the PAN-OS AI agent

**Version**: 1.0
**Last Updated**: 2025-11-07
**Status**: Production-ready

---

## Table of Contents

1. Project Overview

2. Core Architecture  

3. ReAct vs Deterministic: Deep Dive

4. Directory Structure

5. State Management

6. Subgraph Patterns

7. Tool Organization

8. Testing Strategy

9. Common Patterns

10. Troubleshooting

---

## Project Overview

### Purpose

AI-powered automation agent for Palo Alto Networks PAN-OS firewalls using LangGraph and
  pan-os-python.
  Demonstrates two distinct automation approaches:

1. **Autonomous Mode**: ReAct agent with full tool access for exploratory automation

2. **Deterministic Mode**: Predefined workflows for repeatable, auditable operations

### Tech Stack

- **LangGraph** (0.2.50+): State graph orchestration
- **LangChain** (0.3.0+): LLM integration and tool binding
- **Anthropic Claude**: Sonnet 4.5 for reasoning
- **pan-os-python** (1.11+): PAN-OS XML API client
- **Python** 3.11+
- **uv**: Package management
- **pytest**: Testing framework

### Key Metrics

- **33 tools** across 7 categories
- **3 subgraphs** (CRUD, Commit, Deterministic)
- **6 workflows**
- **100% tool error handling** (no exceptions leak to LLM)

---

## Core Architecture

### Composable Subgraph Pattern

```text

Main Graph (checkpointer)
    ├── Autonomous Graph (ReAct loop)
    │   └── Tools → Subgraphs (stateless)
    └── Deterministic Graph (workflow executor)
        └── Workflow Subgraph → Tools → Subgraphs

```text

**Key Principles:**

1. **Checkpointing**: Only main graphs have checkpointers (MemorySaver)

2. **Stateless Subgraphs**: All subgraphs compile without checkpointers

3. **Transactional**: Subgraphs execute atomically within tool calls

4. **Reusable**: Same subgraph can be invoked by multiple tools

### Dual-Mode Design

| Mode | Entry Point | State | Checkpointer | Use Case |
|------|-------------|-------|--------------|----------|
| Autonomous | `autonomous_graph.py` | `AutonomousState` | Yes | Exploration, ad-hoc |
| Deterministic | `deterministic_graph.py` | `DeterministicState` | Yes | Production, repeatable |

---

## ReAct vs Deterministic: Deep Dive

### Overview Comparison

The agent implements two fundamentally different automation paradigms,
  each optimized for different use cases:

| Aspect | Autonomous (ReAct) | Deterministic (Workflow) |
|--------|-------------------|-------------------------|
| **Control Flow** | LLM decides next action | Predefined step sequence |
| **Flexibility** | High - can adapt to any scenario | Medium - follows workflow definition |
| **Predictability** | Variable - depends on LLM reasoning | High - same steps every time |
| **Auditability** | Moderate - log of tool calls | Excellent - known workflow execution |
| **Error Recovery** | LLM can retry/adapt | Stops or continues based on config |
| **Human Approval** | Optional via tools | Built-in approval gates |
| **Tool Access** | All 34 tools available | Only tools in workflow steps |
| **Best For** | Exploration, debugging, ad-hoc tasks | Production, compliance, repeatability |

### Architecture Comparison

#### Autonomous Mode (ReAct Pattern)

**File**: `src/autonomous_graph.py`

**Graph Structure**:

```text

┌─────────────────────────────────────────────────┐
│           Autonomous Graph (ReAct)              │
│  ┌─────────────────────────────────────────┐   │
│  │  1. User Input (HumanMessage)           │   │
│  └─────────────────┬───────────────────────┘   │
│                    │                            │
│                    ▼                            │
│  ┌─────────────────────────────────────────┐   │
│  │  2. Agent Node (LLM with tools)         │   │
│  │     - Receives: messages history        │   │
│  │     - Claude Sonnet 4.5 reasoning       │   │
│  │     - Tool binding (all 34 tools)       │   │
│  │     - Returns: Response + tool calls    │   │
│  └─────────────────┬───────────────────────┘   │
│                    │                            │
│                    ▼                            │
│            ┌───────────────┐                    │
│            │  Tool calls?  │                    │
│            └───────┬───────┘                    │
│                    │                            │
│          ┌─────────┴──────────┐                 │
│          │ Yes                │ No              │
│          ▼                    ▼                 │
│  ┌────────────────┐    ┌──────────────┐        │
│  │  3. Tools Node │    │  5. END      │        │
│  │  Execute tools │    │  (Response)  │        │
│  │  in parallel   │    └──────────────┘        │
│  └────────┬───────┘                            │
│           │                                     │
│           │ 4. Tool results                     │
│           │    added to messages                │
│           └──────────┐                          │
│                      │                          │
│                      ▼                          │
│           ┌────────────────────┐                │
│           │  Loop back to      │                │
│           │  Agent Node (2)    │                │
│           └────────────────────┘                │
│                                                 │
│  State: AutonomousState                        │
│    - messages: List[BaseMessage]               │
│                                                 │
│  Checkpointer: MemorySaver                     │
│    - Persists conversation history             │
│    - Enables multi-turn dialogue               │
└─────────────────────────────────────────────────┘

```text

**Execution Flow**:
1. **User Input**: Natural language prompt → `HumanMessage`

2. **Agent Reasoning**: LLM receives full message history + system prompt + all 34 tools

3. **Decision Point**:

   - If LLM wants more info → calls tools (e.g., `address_list`)
   - If ready to act → calls tools (e.g., `address_create`)
   - If task complete → returns final message
4. **Tool Execution**: Tools execute (may invoke subgraphs), results appended to messages

5. **Loop**: Agent sees tool results, decides next action

6. **Termination**: Agent returns response with no tool calls

**Example Execution**:

```text

User: "Create address objects for web servers 10.1.1.1 through 10.1.1.5"

Turn 1:
  Agent → Thinks: "I need to create 5 address objects"
  Agent → Calls: address_create() for first server
  Tools → Returns: "✅ Created address: web-server-1"

Turn 2:
  Agent → Calls: address_create() for remaining servers (4 more calls)
  Tools → Returns: "✅ Created address" for each

Turn 3:
  Agent → Calls: address_list() to verify all created
  Tools → Returns: List of addresses including new ones

Turn 4:
  Agent → Sees: All addresses created successfully
  Agent → Returns: "I've created 5 address objects for web servers 10.1.1.1 through 10.1.1.5.
  All objects are confirmed."
  END

```text

**Key Characteristics**:
- **Adaptive**: Can change strategy based on results
- **Multi-step**: Automatically breaks complex tasks into steps
- **Self-correcting**: Can retry different approaches on failure
- **Exploratory**: Can list objects, inspect config before acting

#### Deterministic Mode (Workflow Pattern)

**File**: `src/deterministic_graph.py`

**Graph Structure**:

```text

┌──────────────────────────────────────────────────────┐
│        Deterministic Graph (Workflow Executor)       │
│  ┌──────────────────────────────────────────────┐   │
│  │  1. User Input: "workflow: <name>"           │   │
│  └────────────────┬─────────────────────────────┘   │
│                   │                                  │
│                   ▼                                  │
│  ┌──────────────────────────────────────────────┐   │
│  │  2. Load Workflow Definition                 │   │
│  │     - Lookup in WORKFLOWS dict               │   │
│  │     - Extract steps list                     │   │
│  │     - Initialize state                       │   │
│  └────────────────┬─────────────────────────────┘   │
│                   │                                  │
│                   ▼                                  │
│  ┌──────────────────────────────────────────────┐   │
│  │  3. Execute Workflow Subgraph                │   │
│  │  ┌────────────────────────────────────────┐  │   │
│  │  │  Deterministic Workflow Subgraph       │  │   │
│  │  │  ┌──────────────────────────────────┐  │  │   │
│  │  │  │ a. Execute Step                  │  │  │   │
│  │  │  │    - tool_call: Invoke tool      │  │  │   │
│  │  │  │    - approval: Interrupt (HITL)  │  │  │   │
│  │  │  └──────────┬───────────────────────┘  │  │   │
│  │  │             │                           │  │   │
│  │  │             ▼                           │  │   │
│  │  │  ┌──────────────────────────────────┐  │  │   │
│  │  │  │ b. Evaluate Step (LLM)           │  │  │   │
│  │  │  │    - Analyze result              │  │  │   │
│  │  │  │    - Decide: continue/stop/retry │  │  │   │
│  │  │  └──────────┬───────────────────────┘  │  │   │
│  │  │             │                           │  │   │
│  │  │             ▼                           │  │   │
│  │  │      ┌─────────────┐                   │  │   │
│  │  │      │  Continue?  │                   │  │   │
│  │  │      └─────┬───────┘                   │  │   │
│  │  │            │                            │  │   │
│  │  │    ┌───────┴────────┐                  │  │   │
│  │  │    │ Yes            │ No               │  │   │
│  │  │    ▼                ▼                  │  │   │
│  │  │  ┌────────┐   ┌──────────┐            │  │   │
│  │  │  │ Next   │   │ Format   │            │  │   │
│  │  │  │ Step   │   │ Summary  │            │  │   │
│  │  │  └───┬────┘   └────┬─────┘            │  │   │
│  │  │      │             │                   │  │   │
│  │  │      │  Loop       │                   │  │   │
│  │  │      └─────────────┘ END               │  │   │
│  │  └────────────────────────────────────────┘  │   │
│  └──────────────────┬───────────────────────────┘   │
│                     │                                │
│                     ▼                                │
│  ┌──────────────────────────────────────────────┐   │
│  │  4. Return Summary                           │   │
│  │     - Steps executed                         │   │
│  │     - Success/failure counts                 │   │
│  │     - Detailed results                       │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  State: DeterministicState                          │
│    - workflow_steps: List[Dict]                     │
│    - current_step_index: int                        │
│    - step_results: List[Dict]                       │
│                                                      │
│  Checkpointer: MemorySaver                          │
│    - Persists workflow execution state              │
└──────────────────────────────────────────────────────┘

```text

**Workflow Definition Structure**:

```python

{
    "name": "Web Server Setup",
    "description": "Create web server infrastructure",
    "steps": [
        {
            "name": "Create web address",
            "type": "tool_call",
            "tool": "address_create",
            "params": {"name": "web-1", "value": "10.1.1.1"}
        },
        {
            "name": "Create HTTP service",
            "type": "tool_call",
            "tool": "service_create",
            "params": {"name": "http-8080", "protocol": "tcp", "port": "8080"}
        },
        {
            "name": "Approval gate",
            "type": "approval",
            "message": "Objects created. Approve policy creation?"
        },
        {
            "name": "Create security policy",
            "type": "tool_call",
            "tool": "security_policy_create",
            "params": {...}
        }
    ]
}

```text

**Execution Flow**:
1. **Workflow Lookup**: Parse user input → find workflow in `WORKFLOWS` dict

2. **Step Iteration**: Execute each step sequentially

3. **Step Execution**:

   - **tool_call**: Invoke specified tool with params
   - **approval**: Pause for human approval (LangGraph `interrupt()`)
4. **LLM Evaluation**: After each step, LLM analyzes result

   - Success → continue to next step
   - Failure → stop or retry (based on config)
5. **Summary**: Format comprehensive report of execution

**Example Execution**:

```text

User: "workflow: web_server_setup"

Step 1/4: Create web address
  Tool: address_create(name="web-1", value="10.1.1.1")
  Result: ✅ Created address object: web-1
  LLM Evaluation: {"decision": "continue", "success": true}

Step 2/4: Create HTTP service
  Tool: service_create(name="http-8080", protocol="tcp", port="8080")
  Result: ✅ Created service object: http-8080
  LLM Evaluation: {"decision": "continue", "success": true}

Step 3/4: Approval gate
  Type: approval
  PAUSED - Waiting for human approval...
  [User approves]
  Result: User approved continuation

Step 4/4: Create security policy
  Tool: security_policy_create(...)
  Result: ✅ Created security policy rule: allow-web
  LLM Evaluation: {"decision": "continue", "success": true}

Summary:
  📊 Workflow 'web_server_setup' Execution Summary
  Steps: 4/4
  ✅ Successful: 4
  ❌ Failed: 0

```text

**Key Characteristics**:
- **Predictable**: Always executes same steps in same order
- **Auditable**: Clear workflow definition, step-by-step results
- **Gated**: Can require approvals at critical points
- **Repeatable**: Can run same workflow multiple times with different params

### State Management Comparison

#### Autonomous State

```python

class AutonomousState(TypedDict):
    """ReAct agent state - accumulates conversation"""
    messages: Annotated[Sequence[BaseMessage], add_messages]

```text

**Characteristics**:
- **Simple**: Single field (messages)
- **Accumulative**: Messages grow with each turn
- **Stateless subgraphs**: Tools invoke subgraphs without persistent state
- **Conversation-based**: Everything tracked in message history

**State Evolution**:

```text

Turn 1: [HumanMessage("Create address")]
Turn 2: [HumanMessage("Create address"),
         AIMessage(tool_calls=[...]),
         ToolMessage(result="✅ Created")]
Turn 3: [... previous messages ...,
         AIMessage("Address created successfully")]

```text

#### Deterministic State

```python

class DeterministicState(TypedDict):
    """Workflow execution state - tracks step progress"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    workflow_steps: list[dict]           # Predefined steps
    current_step_index: int              # Where we are
    step_results: Annotated[list[dict], operator.add]  # Accumulated results
    continue_workflow: bool              # Should continue?
    workflow_complete: bool              # Finished?
    error_occurred: bool                 # Any failures?

```text

**Characteristics**:
- **Structured**: Multiple fields tracking execution
- **Sequential**: current_step_index increments
- **Result tracking**: step_results accumulates output
- **Workflow-based**: Knows entire execution plan upfront

**State Evolution**:

```text

Initial: {
    workflow_steps: [step1, step2, step3],
    current_step_index: 0,
    step_results: []
}

After Step 1: {
    workflow_steps: [step1, step2, step3],
    current_step_index: 1,
    step_results: [{"step": "step1", "status": "success"}]
}

After Step 2: {
    workflow_steps: [step1, step2, step3],
    current_step_index: 2,
    step_results: [
        {"step": "step1", "status": "success"},
        {"step": "step2", "status": "success"}
    ]
}

Complete: {
    workflow_steps: [step1, step2, step3],
    current_step_index: 3,
    step_results: [...all 3 results...],
    workflow_complete: true
}

```text

### Decision-Making Comparison

#### Autonomous Mode Decision Flow

```text

User Input
    │
    ▼
┌─────────────────────────────────────────┐
│ LLM Reasoning (Claude Sonnet 4.5)      │
│                                         │
│ Context:                                │
│  - System prompt (PAN-OS expert)        │
│  - Full message history                 │
│  - All 34 tool descriptions             │
│  - User's current request               │
│                                         │
│ Decision Process:                       │
│  1. Understand user intent              │
│  2. Assess what info needed             │
│  3. Select appropriate tools            │
│  4. Determine tool parameters           │
│  5. Decide if task complete             │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────┐
│ Decision Types  │
└─────────────────┘
    │
    ├─► Information Gathering
    │   (e.g., list objects before creating)
    │
    ├─► Single Action
    │   (e.g., create one address)
    │
    ├─► Batch Operation
    │   (e.g., create multiple objects)
    │
    ├─► Multi-step Task
    │   (e.g., create objects, then policy, then commit)
    │
    └─► Final Response
        (no more tool calls needed)

```text

**Example Decision Process**:

```text

User: "Set up web server access for 10.1.1.0/24 to internet"

LLM Reasoning:

  1. Need to create source address (10.1.1.0/24)

  2. Need to identify appropriate services (likely HTTP/HTTPS)

  3. Need to create security policy (trust → untrust)

  4. Should verify before committing

Decision: Call tools sequentially
  → address_create(name="internal-web", value="10.1.1.0/24")
  → security_policy_create(source=["internal-web"], ...)
  → Ask user about commit

```text

#### Deterministic Mode Decision Flow

```text

Workflow Definition (Static)
    │
    ▼
┌─────────────────────────────────────────┐
│ Step Executor (No decision making)     │
│                                         │
│ Process:                                │
│  1. Read step definition                │
│  2. Execute exactly as specified        │
│  3. No deviation from workflow          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ LLM Evaluation (After execution)       │
│                                         │
│ Context:                                │
│  - Step definition                      │
│  - Execution result                     │
│  - Success/failure indicators           │
│                                         │
│ Decision:                               │
│  - continue: Success, next step         │
│  - stop: Critical failure, abort        │
│  - retry: Transient error (not impl)    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────┐
│ Decision Types  │
└─────────────────┘
    │
    ├─► Continue
    │   Result looks good → next step
    │
    ├─► Stop
    │   Error occurred → abort workflow
    │
    └─► Pause (approval type)
        Wait for human → then continue

```text

**Example Decision Process**:

```text

Workflow: "complete_security_workflow"

Step 1: Batch create addresses
  Execute: batch_operation(items=[...])
  Result: "✅ Successful: 2"
  LLM Evaluation:

    - Sees "✅" indicator
    - Confirms 2/2 success
    - Decision: continue

Step 2: Create security policy
  Execute: security_policy_create(...)
  Result: "❌ Error: Object 'internal-net-1' does not exist"
  LLM Evaluation:

    - Sees "❌" indicator
    - Detects dependency error
    - Decision: stop

Workflow: STOPPED
Reason: Critical error - missing dependency

```text

### When to Use Each Mode

#### Use Autonomous Mode When:

✅ **Exploratory Tasks**

- "Show me all address objects and groups"
- "Find unused security policies"
- "Investigate why traffic is being blocked"

✅ **Ad-hoc Operations**

- "Create a new address for server X"
- "Quickly add this IP to the DMZ group"
- "Delete all objects with tag 'temporary'"

✅ **Complex Problem-Solving**

- "Set up microsegmentation for database tier"
- "Optimize our security policy rulebase"
- "Troubleshoot connectivity issue between zones"

✅ **Learning/Training**

- "What objects reference this address group?"
- "How would I create a security policy for...?"
- "Explain the current NAT configuration"

✅ **Adaptive Requirements**

- Task requirements not fully known upfront
- Need LLM to make decisions based on current state
- Want agent to explore options and recommend

#### Use Deterministic Mode When:

✅ **Production Workflows**

- Standard server onboarding
- Network segment provisioning
- Scheduled policy updates

✅ **Compliance/Audit**

- Need exact record of steps executed
- Require approval gates
- Must follow specific procedures

✅ **Repeatable Operations**

- Same task performed regularly
- Multiple environments (dev/staging/prod)
- Batch processing with known parameters

✅ **Critical Operations**

- Changes requiring human approval
- Multi-step processes with dependencies
- Operations with rollback requirements

✅ **Team Collaboration**

- Codify team procedures as workflows
- Share standardized automation
- Onboard new team members with workflows

### Performance Characteristics

| Metric | Autonomous | Deterministic |
|--------|-----------|---------------|
| **Tokens per operation** | High (full reasoning each turn) | Medium (evaluation only) |
| **Latency** | Variable (depends on LLM decisions) | Predictable (fixed steps) |
| **Cost** | Higher (more LLM calls) | Lower (fewer LLM calls) |
| **Flexibility** | Maximum | Limited to workflow |
| **Error handling** | Adaptive (LLM can retry) | Fixed (stop or continue) |

### Code Examples

#### Autonomous Mode Invocation

```python

from src.autonomous_graph import create_autonomous_graph
from langchain_core.messages import HumanMessage

# Create graph
graph = create_autonomous_graph()

# Invoke with natural language
result = graph.invoke(
    {"messages": [HumanMessage(content="Create 5 addresses for web servers")]},
    config={"configurable": {"thread_id": "user-123"}}
)

# LLM decides what tools to use
# Might call: batch_operation, address_list, etc.

```text

#### Deterministic Mode Invocation

```python

from src.deterministic_graph import create_deterministic_graph
from langchain_core.messages import HumanMessage

# Create graph
graph = create_deterministic_graph()

# Invoke with workflow name
result = graph.invoke(
    {"messages": [HumanMessage(content="workflow: web_server_setup")]},
    config={"configurable": {"thread_id": "workflow-456"}}
)

# Executes predefined steps exactly as specified

```text

---

## Directory Structure

```python

panos-agent/
├── src/
│   ├── autonomous_graph.py         # ReAct agent (agent → tools → agent)
│   ├── deterministic_graph.py      # Workflow executor
│   ├── core/
│   │   ├── config.py               # Pydantic settings from .env
│   │   ├── client.py               # Singleton PAN-OS firewall client
│   │   ├── state_schemas.py        # All TypedDict state definitions
│   │   ├── retry_helper.py         # Exponential backoff retry
│   │   └── subgraphs/
│   │       ├── crud.py             # Single object lifecycle
│   │       ├── commit.py           # PAN-OS commit with polling
│   │       └── deterministic.py    # Workflow step executor
│   ├── tools/
│   │   ├── address_objects.py      # 5 tools (create/read/update/delete/list)
│   │   ├── address_groups.py       # 5 tools
│   │   ├── services.py             # 5 tools
│   │   ├── service_groups.py       # 5 tools
│   │   ├── security_policies.py    # 5 tools
│   │   ├── nat_policies.py         # 4 tools
│   │   └── orchestration/
│   │       ├── crud_operations.py  # crud_operation (unified)
│   │       └── commit_operations.py # commit_changes
│   ├── workflows/
│   │   └── definitions.py          # 6 predefined workflows
│   └── cli/
│       └── commands.py             # Typer CLI
├── tests/
│   ├── conftest.py                 # Shared fixtures
│   └── ...
├── docs/
│   └── ARCHITECTURE.md             # This file
├── langgraph.json                  # LangGraph Studio config
├── pyproject.toml                  # uv package config
├── .pre-commit-config.yaml         # Code quality hooks
└── README.md

```text

---

## State Management

### State Schema Design

All state schemas defined in `src/core/state_schemas.py` using `TypedDict`.

#### Message Accumulation

```python

from langgraph.graph.message import add_messages

class AutonomousState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

```text

- `add_messages` reducer: Appends new messages to history
- Used in both autonomous and deterministic graphs

#### Parallel Write Reducers

```python

import operator

class BatchState(TypedDict):
    current_batch_results: Annotated[list[dict], operator.add]

```text

- `operator.add` reducer: Allows multiple parallel nodes to write
- Critical for LangGraph `Send` API (fan-out/fan-in)

#### State Lifecycle

1. **Initialization**: Tool/workflow invokes subgraph with initial state

2. **Transformation**: Each node returns updated state dict

3. **Aggregation**: Reducers combine parallel writes

4. **Return**: Final state dict returned to caller

### State Schemas Reference

| Schema | Purpose | Key Fields |
|--------|---------|------------|
| `AutonomousState` | ReAct agent loop | `messages` |
| `DeterministicState` | Workflow execution | `workflow_steps`, `step_results` |
| `CRUDState` | Single object ops | `operation_type`, `object_name`, `data` |
| `BatchState` | Parallel batch ops | `items`, `dependency_levels`, `current_batch_results` |
| `CommitState` | Commit workflow | `description`, `commit_job_id`, `job_status` |

---

## Subgraph Patterns

### CRUD Subgraph

**File**: `src/core/subgraphs/crud.py`

**Purpose**: Single object lifecycle with validation and retry

**Flow**:

```text

validate_input → check_existence →
[create|read|update|delete|list]_object →
format_response → END

```text

**Routing Logic**:

```python

def route_operation(state: CRUDState):
    if state.get("error"):
        return "format_response"
    return {
        "create": "create_object",
        "read": "read_object",
        ...
    }[state["operation_type"]]

```text

**Error Handling**:
- Always returns error in state, never raises
- Uses `with_retry()` for transient failures
- Classifies errors (permanent vs transient)

### Commit Subgraph

**File**: `src/core/subgraphs/commit.py`

**Purpose**: PAN-OS commit with approval and job polling

**Flow**:

```text

validate → check_approval →
execute_commit → poll_job_status →
format_response → END

```text

**Job Polling**:

```python

# Poll every 5 seconds for max 5 minutes
for poll_count in range(60):
    status = get_job_status(job_id)
    if status == "FIN":
        return success
    elif status in ["FAIL", "ERROR"]:
        return failure
    time.sleep(5)

```text

**HITL Approval**:

```python

approval = interrupt({
    "type": "commit_approval",
    "message": "Approve commit?"
})

```text

### Deterministic Workflow Subgraph

**File**: `src/core/subgraphs/deterministic.py`

**Purpose**: Execute predefined workflows step-by-step

**Flow**:

```text

load_workflow → execute_step →
evaluate_step (LLM) →
[increment_step | format_result]

```text

**LLM Evaluation**:

```python

# LLM decides: continue, stop, or retry
evaluation = llm.invoke([
    SystemMessage("Evaluate step result"),
    HumanMessage(f"Step: {step_name}, Result: {result}")
])
# Returns: {"decision": "continue", "reason": "...", "success": true}

```text

---

## Tool Organization

### Tool Categories (34 total)

**Object CRUD** (20 tools):
- Address objects (5)
- Address groups (5)
- Services (5)
- Service groups (5)

**Policy Management** (9 tools):
- Security policies (5: create, read, update, delete, list)
- NAT policies (4: create_source, read, delete, list)

**Orchestration** (3 tools):
- `crud_operation`: Unified CRUD interface
- `batch_operation`: Parallel batch operations
- `commit_changes`: Firewall commit

**Special** (2 tools):
- Policy read-only tools (included in counts above)

### Tool Design Pattern

**Template**:

```python

from langchain_core.tools import tool

@tool
def my_tool(param: str) -> str:
    """Docstring with examples.

    MUST return string, NEVER raise exceptions.
    """
    try:
        result = subgraph.invoke(
            {...},
            config={"configurable": {"thread_id": str(uuid.uuid4())}}
        )
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"

```text

**Key Rules**:
1. **Always return string** (even on error)

2. **Use unique thread_id** for stateless subgraphs

3. **Comprehensive docstrings** with examples

4. **Type hints** for all parameters

5. **Error context** in return message

---

## Testing Strategy

### Test Structure

```text

tests/
├── conftest.py              # Shared fixtures (mock firewall, objects)
├── test_crud_subgraph.py    # Integration tests (with mocks)
├── test_commit_subgraph.py  # Integration tests
└── test_tools.py            # Tool invocation tests

```text

### Fixtures

**Mock Firewall**:

```python

@pytest.fixture
def mock_firewall():
    fw = MagicMock()
    fw.hostname = "192.168.1.1"
    fw.refreshall = Mock()
    fw.find = Mock()
    return fw

```text

**Mock Objects**:
- `mock_address_object`
- `mock_address_group`
- `mock_service_object`
- `mock_security_rule`

**Sample Data**:
- `sample_addresses`
- `sample_services`
- `sample_security_rules`

### Running Tests

```bash

# All tests
pytest

# Specific file
pytest tests/test_crud_subgraph.py

# With coverage
pytest --cov=src --cov-report=html

# Verbose
pytest -v

```text

---

## Common Patterns

### Pattern 1: Subgraph Invocation

```python

import uuid

subgraph = create_my_subgraph()
result = subgraph.invoke(
    {"field": "value"},
    config={"configurable": {"thread_id": str(uuid.uuid4())}}
)
return result["message"]

```text

### Pattern 2: Error Handling in Tools

```python

@tool
def my_tool() -> str:
    try:
        # ... subgraph invocation
        return result["message"]
    except Exception as e:
        return f"❌ Error: {type(e).__name__}: {e}"

```text

### Pattern 3: Conditional Routing

```python

def route_based_on_state(state: MyState):
    if state.get("error"):
        return "error_handler"
    elif state.get("needs_approval"):
        return "request_approval"
    else:
        return "continue"

```text

---

## Troubleshooting

### Issue: tool_use without tool_result

**Symptom**: 400 BadRequest from Anthropic API

**Cause**: Tool raised exception instead of returning string

**Fix**: Wrap all tool calls in try/except, return error string

### Issue: State Not Persisting

**Symptom**: Conversation history lost between turns

**Cause**: Subgraph has its own checkpointer

**Fix**: Remove checkpointer from subgraphs, only use in main graphs

---

## Version History

**v1.0** (2025-11-07):
- Initial production release
- 34 tools, 4 subgraphs, 9 workflows
- Batch operations with dependency resolution
- Commit workflow with job polling
- Comprehensive test suite
- Pre-commit hooks (black, flake8, isort)

---

**For questions or contributions, see main README.md**
