# TODO: PAN-OS Agent Enhancement Roadmap

**Project:** PAN-OS Automation AI Agent
**Version:** 0.1.0 → 1.0.0 (Production-Ready)
**Based on:** LangGraph v1.0.0 Recommendations Review
**Last Updated:** 2025-01-08

---

## Overview

This TODO tracks the implementation of enhancements identified through a comprehensive review of 25 LangGraph v1.0.0 documentation files against the current PAN-OS agent implementation.

### Summary Statistics

- **Total Effort:** 33-51 hours
- **Phases:** 3 (Production Readiness → Robustness → Optional)
- **Major Tasks:** 11
- **Subtasks:** 60+
- **Current Status:** Phase 0 Complete (All core features implemented)

### Quick Navigation

- [Phase 1: Production Readiness (16-24h)](#phase-1-production-readiness-16-24-hours) - CRITICAL
- [Phase 2: Robustness Enhancements (12-18h)](#phase-2-robustness-enhancements-12-18-hours) - HIGH
- [Phase 3: Optional Enhancements (5-9h)](#phase-3-optional-enhancements-5-9-hours) - LOW
- [Completed Work](#completed-work-reference)

---

## Phase 1: Production Readiness (16-24 hours)

**Priority:** CRITICAL - Must complete before production deployment
**Goal:** Address security gaps, add observability, ensure quality

### 1. Observability & Security (4-5 hours)

#### 1.1 Add LangSmith Environment Variables (0.5 hours)

**Priority:** HIGH
**Dependencies:** None
**Can Run in Parallel:** Yes

- [ ] **Update `.env.example`**
  - [ ] Add `LANGSMITH_TRACING=true`
  - [ ] Add `LANGSMITH_API_KEY=lsv2_pt_...` (placeholder)
  - [ ] Add `LANGSMITH_PROJECT=panos-agent-prod`
  - [ ] Add comments explaining each variable
  - **File:** `.env.example`

- [ ] **Update Settings class**
  - [ ] Add `langsmith_tracing: bool` field with default `False`
  - [ ] Add `langsmith_api_key: str | None` field with default `None`
  - [ ] Add `langsmith_project: str` field with default `"panos-agent"`
  - [ ] Add docstrings for observability fields
  - **File:** `src/core/config.py`

**Acceptance Criteria:**

- [ ] All three env vars documented in `.env.example`
- [ ] Settings class loads vars without errors
- [ ] Default values allow running without LangSmith

**References:**

- `docs/recommendations/19-observability.md`

---

#### 1.2 Implement Anonymizers (2-3 hours) ⚠️ CRITICAL SECURITY

**Priority:** CRITICAL (blocks production tracing)
**Dependencies:** Task 1.1 must be complete
**Can Run in Parallel:** No (must finish before enabling tracing)

- [ ] **Create anonymizer module**
  - [ ] Create `src/core/anonymizers.py` file
  - [ ] Import `create_anonymizer` from langchain_core
  - [ ] Import `Client`, `LangChainTracer` from langsmith
  - **File:** `src/core/anonymizers.py` (NEW)

- [ ] **Implement PAN-OS API key pattern**
  - [ ] Pattern: `LUFRPT[A-Za-z0-9+/=]{40,}`
  - [ ] Replace: `<panos-api-key>`
  - [ ] Test with sample API keys

- [ ] **Implement Anthropic API key pattern**
  - [ ] Pattern: `sk-ant-[A-Za-z0-9-_]{40,}`
  - [ ] Replace: `<anthropic-api-key>`
  - [ ] Test with real API key format

- [ ] **Implement password field patterns**
  - [ ] Pattern: `(password|passwd|pwd)['\"]?\s*[:=]\s*['\"]?[^\s'\"]+`
  - [ ] Replace: `\1: <password>`
  - [ ] Case-insensitive flag
  - [ ] Test with various formats (JSON, XML, plain text)

- [ ] **Implement XML password element pattern**
  - [ ] Pattern: `<password>.*?</password>`
  - [ ] Replace: `<password><redacted></password>`
  - [ ] Test with PAN-OS API response samples

- [ ] **Create anonymizer factory function**
  - [ ] Function: `create_panos_anonymizer() -> LangChainTracer`
  - [ ] Combine all patterns into anonymizer
  - [ ] Return configured LangChainTracer with client
  - [ ] Add comprehensive docstring with examples

- [ ] **Write unit tests**
  - [ ] Create `tests/unit/test_anonymizers.py`
  - [ ] Test each pattern individually
  - [ ] Test combined patterns
  - [ ] Test with real-world trace samples
  - [ ] Verify no false positives (don't mask legitimate data)
  - **File:** `tests/unit/test_anonymizers.py` (NEW)

- [ ] **Integration test with LangSmith**
  - [ ] Enable tracing with anonymizer in test environment
  - [ ] Send test data with sensitive info
  - [ ] Verify trace in LangSmith UI shows masked values
  - [ ] Document test procedure

**Acceptance Criteria:**

- [ ] All 4 sensitive data patterns detected and masked
- [ ] No false positives (legitimate data not masked)
- [ ] Unit tests achieve 100% pattern coverage
- [ ] Integration test confirms no leaks to LangSmith
- [ ] Code includes usage examples in docstring

**References:**

- `docs/recommendations/19-observability.md` (lines 78-145)
- LangSmith anonymizers: <https://docs.smith.langchain.com/how_to_guides/anonymization>

---

#### 1.3 Add Metadata and Tags to Graph Invocations (1 hour)

**Priority:** HIGH
**Dependencies:** Tasks 1.1-1.2 must be complete
**Can Run in Parallel:** After anonymizers are complete

- [ ] **Update autonomous mode invocation**
  - [ ] Add `tags` list: `["panos-agent", "autonomous", "v0.1.0"]`
  - [ ] Add `metadata` dict with:
    - `mode`: "autonomous"
    - `thread_id`: tid
    - `firewall_host`: settings.panos_hostname
    - `user_prompt_length`: len(prompt)
    - `timestamp`: ISO format
  - **File:** `src/cli/commands.py` (line ~70)

- [ ] **Update deterministic mode invocation**
  - [ ] Add `tags` list: `["panos-agent", "deterministic", workflow_name, "v0.1.0"]`
  - [ ] Add `metadata` dict with:
    - `mode`: "deterministic"
    - `workflow`: workflow_name
    - `thread_id`: tid
    - `firewall_host`: settings.panos_hostname
    - `total_steps`: len(workflow_def.get("steps", []))
    - `timestamp`: ISO format
  - **File:** `src/cli/commands.py` (line ~101)

- [ ] **Update README.md with observability section**
  - [ ] Add "Observability" section
  - [ ] Document metadata fields and their purposes
  - [ ] Show how to filter traces by tags in LangSmith
  - [ ] Include screenshot or example trace URL
  - **File:** `README.md`

**Acceptance Criteria:**

- [ ] Both modes send tags and metadata
- [ ] Metadata includes all specified fields
- [ ] Tags allow easy filtering in LangSmith UI
- [ ] Documentation explains observability features

**References:**

- `docs/recommendations/19-observability.md` (lines 147-187)

---

### 2. Testing Infrastructure (8-12 hours)

#### 2.1 Create Unit Tests for Nodes and Tools (4-6 hours)

**Priority:** HIGH
**Dependencies:** None
**Can Run in Parallel:** Yes

- [ ] **Set up test infrastructure**
  - [ ] Create `tests/unit/` directory if not exists
  - [ ] Create `tests/unit/__init__.py`
  - [ ] Create `tests/unit/conftest.py` with shared fixtures
  - [ ] Add pytest-mock to dev dependencies if needed
  - **Files:** `tests/unit/conftest.py` (NEW)

- [ ] **Create test file for autonomous graph nodes**
  - [ ] Create `tests/unit/test_autonomous_nodes.py`
  - [ ] Import node functions: `call_agent`, `route_after_agent`
  - [ ] Create mock state fixtures
  - **File:** `tests/unit/test_autonomous_nodes.py` (NEW)

- [ ] **Test `call_agent` node**
  - [ ] Test with simple query (no tool calls expected)
  - [ ] Test state structure: `{"messages": [HumanMessage(content="...")]}`
  - [ ] Assert returns dict with "messages" key
  - [ ] Assert response is AIMessage
  - [ ] Mock LLM to avoid API calls (use pytest-mock)

- [ ] **Test `route_after_agent` function**
  - [ ] Test routing to "tools" when tool_calls present
  - [ ] Test routing to END when no tool_calls
  - [ ] Test with empty tool_calls list → END
  - [ ] Test with multiple tool_calls → "tools"

- [ ] **Create test file for deterministic graph nodes**
  - [ ] Create `tests/unit/test_deterministic_nodes.py`
  - [ ] Import: `load_workflow_definition`, `route_after_load`
  - **File:** `tests/unit/test_deterministic_nodes.py` (NEW)

- [ ] **Test workflow loading**
  - [ ] Test valid workflow JSON
  - [ ] Test invalid workflow (missing required fields)
  - [ ] Test workflow parsing errors
  - [ ] Assert state updates correctly

- [ ] **Create test file for tools**
  - [ ] Create `tests/unit/test_tools.py`
  - [ ] Import representative tools from each category
  - **File:** `tests/unit/test_tools.py` (NEW)

- [ ] **Test tool invocations**
  - [ ] Test each tool returns string (never raises)
  - [ ] Test tool error handling (invalid params → error message string)
  - [ ] Test successful tool execution format
  - [ ] Mock PAN-OS client to avoid API calls

- [ ] **Create test file for subgraph nodes**
  - [ ] Create `tests/unit/test_subgraphs.py`
  - [ ] Test CRUD subgraph nodes
  - [ ] Test commit subgraph nodes
  - **File:** `tests/unit/test_subgraphs.py` (NEW)

- [ ] **Calculate and verify coverage**
  - [ ] Run: `pytest --cov=src/autonomous_graph --cov=src/deterministic_graph --cov=src/core/tools tests/unit/`
  - [ ] Achieve >80% coverage on critical paths
  - [ ] Generate coverage report: `pytest --cov-report=html`

**Acceptance Criteria:**

- [ ] All node functions have unit tests
- [ ] All routing functions tested
- [ ] Representative tool tests cover all categories
- [ ] >80% code coverage on graph modules
- [ ] All tests pass: `pytest tests/unit/ -v`
- [ ] Tests use mocks (no real API calls)

**References:**

- `docs/recommendations/16-test.md` (lines 79-139)
- LangGraph testing: <https://langchain-ai.github.io/langgraph/how-tos/testing/>

---

#### 2.2 Create Integration Tests for Full Graphs (3-4 hours)

**Priority:** HIGH
**Dependencies:** Task 2.1 should be mostly complete (fixtures available)
**Can Run in Parallel:** After unit test infrastructure exists

- [ ] **Set up integration test infrastructure**
  - [ ] Create `tests/integration/` directory
  - [ ] Create `tests/integration/__init__.py`
  - [ ] Create `tests/integration/conftest.py` with graph fixtures
  - **Files:** `tests/integration/conftest.py` (NEW)

- [ ] **Create graph fixtures**
  - [ ] Fixture: `autonomous_graph()` → compiled graph
  - [ ] Fixture: `deterministic_graph()` → compiled graph
  - [ ] Fixture: `test_thread_id()` → unique thread ID
  - [ ] Mock PAN-OS client globally for integration tests

- [ ] **Create autonomous graph integration tests**
  - [ ] Create `tests/integration/test_autonomous_graph.py`
  - **File:** `tests/integration/test_autonomous_graph.py` (NEW)

- [ ] **Test autonomous graph end-to-end**
  - [ ] Test: Simple query without tools
    - Input: "Hello"
    - Assert: Response received, no tool calls
  - [ ] Test: Query triggering single tool
    - Input: "List address objects"
    - Assert: Tool called, result returned
  - [ ] Test: Query triggering multiple tool calls
    - Input: "Create address objects A, B, C"
    - Assert: Multiple tools executed, all results aggregated
  - [ ] Test: Checkpointing works
    - Invoke with thread_id
    - Invoke again with same thread_id
    - Assert: History preserved

- [ ] **Create deterministic graph integration tests**
  - [ ] Create `tests/integration/test_deterministic_graph.py`
  - **File:** `tests/integration/test_deterministic_graph.py` (NEW)

- [ ] **Test deterministic graph end-to-end**
  - [ ] Test: Simple workflow (1-2 steps)
    - Input: Workflow JSON with basic steps
    - Assert: All steps executed, results tracked
  - [ ] Test: Workflow with error handling
    - Input: Workflow with step that fails
    - Assert: Error captured, workflow stops gracefully
  - [ ] Test: Workflow state management
    - Assert: `workflow_steps`, `step_results`, `current_step` updated correctly

- [ ] **Test subgraphs in integration**
  - [ ] Test CRUD subgraph invocation from autonomous graph
  - [ ] Test commit subgraph with interrupt (mock approval)

- [ ] **Run full integration suite**
  - [ ] Run: `pytest tests/integration/ -v --tb=short`
  - [ ] Verify all tests pass
  - [ ] Check execution time (should be <30s for all)

**Acceptance Criteria:**

- [ ] End-to-end tests for both graph modes
- [ ] Tests verify state management and checkpointing
- [ ] Tests verify tool execution and result aggregation
- [ ] All integration tests pass
- [ ] Tests complete in reasonable time (<30s total)

**References:**

- `docs/recommendations/16-test.md` (lines 141-191)

---

#### 2.3 Set Up LangSmith Evaluation (1-2 hours)

**Priority:** MEDIUM-HIGH
**Dependencies:** Tasks 1.1-1.3 must be complete (LangSmith enabled)
**Can Run in Parallel:** After observability is set up

- [ ] **Create evaluation dataset**
  - [ ] Log into LangSmith UI
  - [ ] Create dataset: "panos-agent-eval-v1"
  - [ ] Add 10-15 representative examples:
    - Simple queries (list, show)
    - CRUD operations (create, update, delete)
    - Complex workflows (multi-step)
    - Error cases (invalid input)
  - [ ] Tag examples by category: "simple", "crud", "workflow", "error"

- [ ] **Define success metrics**
  - [ ] Tool usage accuracy (correct tool selected)
  - [ ] Response completeness (all requested info provided)
  - [ ] Error handling (graceful failures)
  - [ ] Token efficiency (cost per operation)

- [ ] **Create evaluation script**
  - [ ] Create `scripts/evaluate.py`
  - [ ] Load evaluation dataset from LangSmith
  - [ ] Run agent on each example
  - [ ] Collect metrics
  - [ ] Report results
  - **File:** `scripts/evaluate.py` (NEW)

- [ ] **Set up regression alerts**
  - [ ] Configure LangSmith alerts for:
    - Success rate drops below 90%
    - Average token usage increases >20%
    - Error rate increases >5%
  - [ ] Document alert setup in README

- [ ] **Document evaluation process**
  - [ ] Add "Evaluation" section to README
  - [ ] Show how to run evaluation: `python scripts/evaluate.py`
  - [ ] Explain metrics and thresholds
  - **File:** `README.md`

**Acceptance Criteria:**

- [ ] Evaluation dataset exists in LangSmith with 10+ examples
- [ ] Evaluation script runs successfully
- [ ] Metrics tracked: success rate, token usage, error rate
- [ ] Alerts configured in LangSmith
- [ ] Process documented in README

**References:**

- `docs/recommendations/16-test.md` (lines 193-215)
- LangSmith evaluation: <https://docs.smith.langchain.com/evaluation>

---

### 3. Error Handling & Resilience (4-6 hours)

#### 3.1 Add Timeout Handling to Graph Invocations (1 hour)

**Priority:** MEDIUM-HIGH
**Dependencies:** None
**Can Run in Parallel:** Yes

- [ ] **Define timeout constants**
  - [ ] Add to `src/core/config.py` or `src/cli/commands.py`
  - [ ] `TIMEOUT_AUTONOMOUS = 300.0` # 5 minutes
  - [ ] `TIMEOUT_DETERMINISTIC = 600.0` # 10 minutes
  - [ ] `TIMEOUT_COMMIT = 180.0` # 3 minutes
  - [ ] Add docstrings explaining timeout rationale
  - **File:** `src/core/config.py`

- [ ] **Apply timeout to autonomous invocation**
  - [ ] Add `timeout` to config dict
  - [ ] Use `TIMEOUT_AUTONOMOUS` constant
  - [ ] Add try/except for TimeoutError
  - [ ] Log timeout with context (thread_id, prompt preview)
  - **File:** `src/cli/commands.py` (line ~70)

- [ ] **Apply timeout to deterministic invocation**
  - [ ] Add `timeout` to config dict
  - [ ] Use `TIMEOUT_DETERMINISTIC` constant
  - [ ] Add try/except for TimeoutError
  - [ ] Log timeout with context (thread_id, workflow name)
  - **File:** `src/cli/commands.py` (line ~101)

- [ ] **Document timeout behavior**
  - [ ] Add "Timeouts" section to README
  - [ ] Explain default timeouts for each mode
  - [ ] Show how to override: `config={"timeout": 900.0}`
  - **File:** `README.md`

**Acceptance Criteria:**

- [ ] Timeouts configured for both modes
- [ ] TimeoutError caught and logged gracefully
- [ ] User-friendly error message on timeout
- [ ] Documented in README

**References:**

- `docs/recommendations/08-durable-execution.md` (lines 79-106)

---

#### 3.2 Add Retry Policies for PAN-OS API Operations (2-3 hours)

**Priority:** MEDIUM-HIGH
**Dependencies:** None
**Can Run in Parallel:** Yes

- [ ] **Define retry policy**
  - [ ] Create `src/core/retry_policies.py`
  - [ ] Import `RetryPolicy` from langgraph.pregel
  - [ ] Import PAN-OS exceptions: `PanDeviceError`, `PanConnectionError`
  - **File:** `src/core/retry_policies.py` (NEW)

- [ ] **Create PAN-OS retry policy**
  - [ ] Policy name: `PANOS_RETRY_POLICY`
  - [ ] `max_attempts=3`
  - [ ] `retry_on=(PanDeviceError, ConnectionError, TimeoutError)`
  - [ ] `backoff_factor=2.0` (exponential: 2s, 4s, 8s)
  - [ ] Add docstring with retry behavior explanation

- [ ] **Apply retry policy to tool node**
  - [ ] Import `PANOS_RETRY_POLICY` in autonomous_graph.py
  - [ ] Add `retry=PANOS_RETRY_POLICY` to `add_node("tools", ...)` call
  - [ ] Test with mock transient failure
  - **File:** `src/autonomous_graph.py` (line ~120)

- [ ] **Apply retry policy to deterministic workflow node**
  - [ ] Import `PANOS_RETRY_POLICY` in deterministic.py subgraph
  - [ ] Add retry to `execute_step` node
  - [ ] Test with mock transient failure
  - **File:** `src/core/subgraphs/deterministic.py`

- [ ] **Apply retry policy to CRUD subgraph**
  - [ ] Add retry to `execute_operation` node
  - [ ] Test CRUD operations with simulated failures
  - **File:** `src/core/subgraphs/crud.py`

- [ ] **Add logging for retries**
  - [ ] Log retry attempts: "Retrying operation (attempt 2/3)"
  - [ ] Log final failure after max attempts
  - [ ] Include operation context in logs

- [ ] **Document retry behavior**
  - [ ] Add "Error Handling" section to README
  - [ ] Explain retry policy (what errors, how many attempts, backoff)
  - [ ] Note that retries are automatic and transparent
  - **File:** `README.md`

**Acceptance Criteria:**

- [ ] Retry policy defined with exponential backoff
- [ ] Applied to all PAN-OS API operation nodes
- [ ] Retries logged with attempt count
- [ ] Documented in README
- [ ] Integration test verifies retry on transient failure

**References:**

- `docs/recommendations/08-durable-execution.md` (lines 108-155)
- `docs/recommendations/21-use-the-graph-api.md` (lines 189-225)

---

#### 3.3 Document Resume Strategies After Failures (1 hour)

**Priority:** MEDIUM
**Dependencies:** None
**Can Run in Parallel:** Yes

- [ ] **Add "Recovering from Failures" section to README**
  - [ ] Explain checkpointing and resume capability
  - [ ] Show resume command example
  - [ ] Explain thread_id importance
  - **File:** `README.md`

- [ ] **Create troubleshooting guide**
  - [ ] Create `docs/TROUBLESHOOTING.md`
  - [ ] Common errors and solutions
  - [ ] How to resume from checkpoint
  - [ ] How to view checkpoint history
  - [ ] How to reset state (new thread_id)
  - **File:** `docs/TROUBLESHOOTING.md` (NEW)

- [ ] **Add examples to documentation**
  - [ ] Example: Resume after timeout
  - [ ] Example: Resume after network error
  - [ ] Example: Resume after tool failure
  - [ ] Example: Fork from earlier checkpoint (time-travel)

**Acceptance Criteria:**

- [ ] README has recovery section
- [ ] TROUBLESHOOTING.md created with 5+ scenarios
- [ ] Examples show thread_id usage for resume
- [ ] Links between README and TROUBLESHOOTING.md

**References:**

- `docs/recommendations/08-durable-execution.md` (lines 157-189)

---

## Phase 2: Robustness Enhancements (12-18 hours)

**Priority:** HIGH (non-blocking for production, but high value)
**Goal:** Improve context awareness, flexibility, user experience

### 4. Implement Store API for Long-Term Memory (6-8 hours)

**Priority:** MEDIUM
**Dependencies:** None
**Can Run in Parallel:** Yes (independent of other Phase 2 tasks)

- [ ] **Design namespace schema**
  - [ ] Create `docs/MEMORY_SCHEMA.md` to document design
  - [ ] Namespace structure:
    - `("firewall_configs", hostname)` → firewall-specific state
    - `("workflow_history", workflow_name)` → workflow execution history
    - `("user_preferences", user_id)` → user settings (future)
  - [ ] Key structure:
    - `{"config_type": "address_objects"}` → object type
    - `{"execution_id": uuid}` → workflow run
  - **File:** `docs/MEMORY_SCHEMA.md` (NEW)

- [ ] **Create memory store module**
  - [ ] Create `src/core/memory_store.py`
  - [ ] Import `InMemoryStore` from langgraph.store.memory
  - [ ] Create singleton store instance: `get_store() -> InMemoryStore`
  - [ ] Add helper functions:
    - `store_firewall_config(hostname, config_type, data)`
    - `retrieve_firewall_config(hostname, config_type)`
    - `store_workflow_execution(workflow_name, execution_data)`
    - `search_workflow_history(workflow_name, limit=10)`
  - **File:** `src/core/memory_store.py` (NEW)

- [ ] **Update autonomous graph to use Store**
  - [ ] Add `store` parameter to StateGraph creation
  - [ ] Update `call_agent` signature: `def call_agent(state, *, store: BaseStore)`
  - [ ] Store firewall state after operations
  - [ ] Retrieve previous context before operations
  - **File:** `src/autonomous_graph.py`

- [ ] **Update deterministic graph to use Store**
  - [ ] Add `store` parameter to StateGraph creation
  - [ ] Store workflow execution metadata
  - [ ] Store step results for history
  - **File:** `src/deterministic_graph.py`

- [ ] **Add memory context to agent prompts**
  - [ ] In `call_agent`, retrieve recent firewall operations
  - [ ] Add context to system message: "Recent operations on this firewall: ..."
  - [ ] Include counts: "Previously created 5 address objects, updated 2 policies"

- [ ] **Create tests for Store API**
  - [ ] Create `tests/unit/test_memory_store.py`
  - [ ] Test store/retrieve operations
  - [ ] Test search functionality
  - [ ] Test namespace isolation
  - **File:** `tests/unit/test_memory_store.py` (NEW)

- [ ] **Document memory features**
  - [ ] Add "Memory & Context" section to README
  - [ ] Explain what data is remembered
  - [ ] Show how to query memory (future CLI command)
  - [ ] Explain data persistence (in-memory vs persistent store)
  - **File:** `README.md`

**Acceptance Criteria:**

- [ ] Store API integrated into both graphs
- [ ] Firewall config and workflow history stored
- [ ] Agent uses memory context in prompts
- [ ] Memory schema documented
- [ ] Unit tests verify store operations
- [ ] README explains memory features

**References:**

- `docs/recommendations/12-add-memory.md` (lines 79-154)
- Store API: <https://langchain-ai.github.io/langgraph/how-tos/memory/>

---

### 5. Add Runtime Context for LLM Configuration (2-4 hours)

**Priority:** MEDIUM
**Dependencies:** None
**Can Run in Parallel:** Yes

- [ ] **Create runtime context schema**
  - [ ] Create or update `src/core/config.py`
  - [ ] Add dataclass: `AgentContext`
  - [ ] Fields:
    - `model_name: str = "claude-3-5-sonnet-20241022"`
    - `temperature: float = 0.0`
    - `max_tokens: int = 4096`
    - `firewall_client: Any | None = None` (for testing)
  - [ ] Add docstring explaining runtime context vs state
  - **File:** `src/core/config.py`

- [ ] **Update autonomous graph to use runtime context**
  - [ ] Add `context_schema=AgentContext` to StateGraph creation
  - [ ] Update `call_agent` signature: `def call_agent(state, runtime: Runtime[AgentContext])`
  - [ ] Use `runtime.context.model_name` instead of hardcoded model
  - [ ] Use `runtime.context.temperature`
  - [ ] Use `runtime.context.max_tokens`
  - **File:** `src/autonomous_graph.py`

- [ ] **Add CLI flag for model selection**
  - [ ] Add `--model` option to CLI
  - [ ] Choices: `sonnet`, `opus`, `haiku`
  - [ ] Map to full model names
  - [ ] Pass as context in invoke: `context={"model_name": model_full_name}`
  - **File:** `src/cli/commands.py`

- [ ] **Add CLI flag for temperature**
  - [ ] Add `--temperature` option (default 0.0)
  - [ ] Range: 0.0 to 1.0
  - [ ] Pass as context: `context={"temperature": temp}`
  - **File:** `src/cli/commands.py`

- [ ] **Create examples with different models**
  - [ ] Example: `panos-agent "List objects" --model haiku` (fast, cheap)
  - [ ] Example: `panos-agent "Complex workflow" --model sonnet` (default)
  - [ ] Example: `panos-agent "Creative task" --temperature 0.7`

- [ ] **Document runtime context**
  - [ ] Add "Model Selection" section to README
  - [ ] Explain when to use Haiku vs Sonnet
  - [ ] Show CLI flags: `--model`, `--temperature`
  - [ ] Note cost/speed tradeoffs
  - **File:** `README.md`

**Acceptance Criteria:**

- [ ] Runtime context implemented with AgentContext
- [ ] CLI supports model and temperature selection
- [ ] Agent respects context overrides
- [ ] Documented with examples
- [ ] Backwards compatible (defaults work without context)

**References:**

- `docs/recommendations/20-graph-api.md` (lines 99-156)

---

### 6. Add Recursion Limit Handling for Long Workflows (2-3 hours)

**Priority:** MEDIUM
**Dependencies:** Task 5 should be complete (need RunnableConfig in nodes)
**Can Run in Parallel:** After runtime context is implemented

- [ ] **Add recursion check to workflow nodes**
  - [ ] Update `execute_step` signature: `def execute_step(state, config: RunnableConfig)`
  - [ ] Access current step: `config["metadata"]["langgraph_step"]`
  - [ ] Access limit: `config.get("recursion_limit", 25)`
  - [ ] Calculate threshold: `limit * 0.8` (80%)
  - [ ] If approaching limit, return partial result
  - **File:** `src/core/subgraphs/deterministic.py`

- [ ] **Implement graceful stopping**
  - [ ] If step >= threshold:
    - Log warning with current/total steps
    - Return `{"overall_result": {"status": "partial", "reason": "recursion_limit"}}`
    - Return user-friendly message explaining partial completion
  - [ ] Update routing to handle "partial" status → END

- [ ] **Set appropriate recursion limits**
  - [ ] Autonomous mode: Keep default 25 (agent loops should be short)
  - [ ] Deterministic mode: Increase to 50
  - [ ] Add to config in CLI: `config={"recursion_limit": 50}`
  - **File:** `src/cli/commands.py`

- [ ] **Add logging for recursion tracking**
  - [ ] Log every 5 steps: "Workflow progress: 5/50 steps"
  - [ ] Log at 50% threshold: "Workflow at 50% of recursion limit"
  - [ ] Log at 80% threshold: "Approaching recursion limit (40/50)"

- [ ] **Document recursion limits**
  - [ ] Add "Workflow Limits" section to README
  - [ ] Explain default limits (25 autonomous, 50 deterministic)
  - [ ] Show how to increase: `--recursion-limit 100`
  - [ ] Explain graceful degradation (partial results)
  - **File:** `README.md`

- [ ] **Add test for long workflow**
  - [ ] Create test workflow with 30 steps
  - [ ] Run with limit=25
  - [ ] Assert partial completion status
  - [ ] Assert meaningful error message
  - **File:** `tests/integration/test_deterministic_graph.py`

**Acceptance Criteria:**

- [ ] Recursion checks in workflow execution nodes
- [ ] Graceful stopping at 80% threshold
- [ ] User-friendly partial completion message
- [ ] Deterministic mode uses limit=50
- [ ] Documented in README
- [ ] Test verifies graceful handling

**References:**

- `docs/recommendations/20-graph-api.md` (lines 175-236)

---

### 7. Document Deployment to LangSmith (1-2 hours)

**Priority:** MEDIUM
**Dependencies:** Task 1.1-1.3 (observability must be implemented)
**Can Run in Parallel:** After Phase 1 complete

- [ ] **Add "Deployment" section to README**
  - [ ] Prerequisites (LangSmith account, GitHub repo)
  - [ ] Step-by-step deployment process
  - [ ] Show `langgraph deploy` command
  - [ ] Show deployed agent URL
  - **File:** `README.md`

- [ ] **Create deployment guide**
  - [ ] Create `docs/DEPLOYMENT.md`
  - [ ] Detailed deployment steps
  - [ ] Environment variable configuration
  - [ ] LangSmith project setup
  - [ ] API authentication
  - **File:** `docs/DEPLOYMENT.md` (NEW)

- [ ] **Create API usage examples**
  - [ ] Create `examples/api_usage.py`
  - [ ] Example: Python SDK client
  - [ ] Example: Create thread
  - [ ] Example: Run agent
  - [ ] Example: Stream responses
  - [ ] Example: List threads
  - [ ] Example: Get checkpoint history
  - **File:** `examples/api_usage.py` (NEW)

- [ ] **Document REST API endpoints**
  - [ ] Add to DEPLOYMENT.md
  - [ ] Show curl examples:
    - POST /threads
    - POST /threads/{thread_id}/runs
    - GET /threads/{thread_id}/state
    - GET /threads/{thread_id}/history
  - **File:** `docs/DEPLOYMENT.md`

- [ ] **Create deployment checklist**
  - [ ] Pre-deployment checks (tests pass, docs updated)
  - [ ] Deployment steps
  - [ ] Post-deployment validation
  - [ ] Rollback procedure
  - **File:** `docs/DEPLOYMENT.md`

**Acceptance Criteria:**

- [ ] README has deployment section
- [ ] DEPLOYMENT.md comprehensive guide
- [ ] API usage examples work with deployed agent
- [ ] Deployment checklist complete
- [ ] REST API documented with curl examples

**References:**

- `docs/recommendations/17-deploy.md` (lines 79-187)
- LangGraph deploy: <https://langchain-ai.github.io/langgraph/cloud/deployment/>

---

### 8. Enhance Streaming UX for Real-Time Feedback (2-3 hours)

**Priority:** MEDIUM-HIGH
**Dependencies:** None
**Can Run in Parallel:** Yes

- [ ] **Replace `.invoke()` with `.stream()` in autonomous mode**
  - [ ] Change invocation to: `graph.stream(input, config, stream_mode="updates")`
  - [ ] Iterate over chunks: `for chunk in graph.stream(...)`
  - [ ] Display each node's output as it completes
  - [ ] Show progress: "🔄 Agent thinking...", "🔧 Executing tools...", "✅ Complete"
  - **File:** `src/cli/commands.py`

- [ ] **Replace `.invoke()` with `.stream()` in deterministic mode**
  - [ ] Use `stream_mode="updates"`
  - [ ] Display step-by-step progress
  - [ ] Show: "Step 1/5: Creating address object..."
  - [ ] Show: "Step 2/5: Updating security policy..."
  - **File:** `src/cli/commands.py`

- [ ] **Add streaming mode flag**
  - [ ] Add CLI flag: `--no-stream` to disable streaming (use old .invoke())
  - [ ] Default to streaming for better UX
  - [ ] Useful for CI/CD (disable streaming in automation)

- [ ] **Improve output formatting for streaming**
  - [ ] Use Rich library for progress bars (optional)
  - [ ] Color-coded output: 🟢 success, 🟡 in-progress, 🔴 error
  - [ ] Clear visual separation between steps

- [ ] **Add streaming examples to README**
  - [ ] Show streaming output example
  - [ ] Explain real-time feedback benefits
  - [ ] Show how to disable: `--no-stream`
  - **File:** `README.md`

**Acceptance Criteria:**

- [ ] Both modes use streaming by default
- [ ] Real-time progress feedback visible
- [ ] Output clearly shows what's happening
- [ ] `--no-stream` flag works for automation
- [ ] Documented with examples

**References:**

- `docs/recommendations/SUMMARY.md` (Streaming UX section)
- `docs/recommendations/09-streaming.md`

---

## Phase 3: Optional Enhancements (5-9 hours)

**Priority:** LOW - Nice-to-have features for power users
**Goal:** Enhanced developer experience and advanced features

### 9. Document Agent Chat UI Integration (1-2 hours)

**Priority:** LOW
**Dependencies:** Task 1.1-1.3 (observability must work with `langgraph dev`)
**Can Run in Parallel:** Yes

- [ ] **Test Agent Chat UI with local server**
  - [ ] Run: `langgraph dev`
  - [ ] Visit: <https://agentchat.vercel.app>
  - [ ] Connect to: <http://localhost:8000>
  - [ ] Test conversation, tool visualization, time-travel

- [ ] **Add "Agent Chat UI" section to README**
  - [ ] Explain what Agent Chat UI provides
  - [ ] Show hosted option (agentchat.vercel.app)
  - [ ] Show local option (clone repo, npm run dev)
  - [ ] Include screenshots or GIF demo
  - **File:** `README.md`

- [ ] **Document local setup**
  - [ ] Prerequisites: Node.js, npm
  - [ ] Steps:
    - `git clone https://github.com/langchain-ai/agent-chat-ui`
    - `cd agent-chat-ui && npm install`
    - `VITE_LANGGRAPH_API_URL=http://localhost:8000 npm run dev`
  - [ ] Open: <http://localhost:5173>

- [ ] **Create demo video or screenshots**
  - [ ] Screenshot: Tool call visualization
  - [ ] Screenshot: Time-travel debugging
  - [ ] Screenshot: State inspection
  - [ ] Add to `docs/images/` directory
  - **Files:** `docs/images/agent-chat-*.png` (NEW)

**Acceptance Criteria:**

- [ ] Tested with hosted Agent Chat UI
- [ ] Local setup documented
- [ ] README has Agent Chat UI section
- [ ] Screenshots or demo video included

**References:**

- `docs/recommendations/18-agent-chat-ui.md`
- Agent Chat UI: <https://github.com/langchain-ai/agent-chat-ui>

---

### 10. Add Node Caching for Expensive Operations (1-2 hours)

**Priority:** LOW
**Dependencies:** None
**Can Run in Parallel:** Yes

- [ ] **Identify cacheable operations**
  - [ ] Analysis: Most PAN-OS operations are writes (not cacheable)
  - [ ] Potential candidates:
    - List operations (list_address_objects, list_policies)
    - Get operations (get_system_info)
  - [ ] Decision: Only cache if performance issues arise

- [ ] **Implement cache policy (if needed)**
  - [ ] Import `InMemoryCache` from langgraph.cache.memory
  - [ ] Import `CachePolicy` from langgraph.types
  - [ ] Create policy: `CachePolicy(ttl=60)` # 60 second TTL
  - [ ] Apply to read-only tool nodes
  - **File:** `src/autonomous_graph.py` (conditionally)

- [ ] **Benchmark with and without caching**
  - [ ] Measure: Repeated list operations
  - [ ] Compare: Response time, API call count
  - [ ] Decision: Only implement if >20% improvement

- [ ] **Document caching (if implemented)**
  - [ ] Explain which operations are cached
  - [ ] Explain TTL and invalidation
  - [ ] Show how to disable caching (for testing)
  - **File:** `README.md`

**Acceptance Criteria:**

- [ ] Benchmarks show caching provides value (>20% improvement)
- [ ] Cache policy applied to read operations only
- [ ] TTL set appropriately (60s for configs, 300s for system info)
- [ ] Documented if implemented

**References:**

- `docs/recommendations/20-graph-api.md` (lines 322-367)

**Note:** Only implement if benchmarks show significant benefit. Most operations are writes.

---

### 11. Add Time-Travel CLI Commands (2-3 hours)

**Priority:** LOW
**Dependencies:** None (infrastructure already exists via checkpointer)
**Can Run in Parallel:** Yes

- [ ] **Add `history` command**
  - [ ] CLI: `panos-agent history --thread-id abc123`
  - [ ] Show checkpoint history for thread
  - [ ] Display: checkpoint_id, node, timestamp, summary
  - [ ] Use: `graph.get_state_history(config)`
  - **File:** `src/cli/commands.py`

- [ ] **Add `show-checkpoint` command**
  - [ ] CLI: `panos-agent show-checkpoint --thread-id abc123 --checkpoint-id xyz`
  - [ ] Display full state at checkpoint
  - [ ] Show: messages, workflow_steps, results
  - [ ] Use: `graph.get_state(config, checkpoint_id=checkpoint_id)`
  - **File:** `src/cli/commands.py`

- [ ] **Add `fork` command**
  - [ ] CLI: `panos-agent fork --from-thread abc123 --from-checkpoint xyz --to-thread def456`
  - [ ] Create new thread from historical checkpoint
  - [ ] Allow exploration: "What if I did X instead?"
  - [ ] Use: `graph.update_state(new_config, state, as_node="__start__")`
  - **File:** `src/cli/commands.py`

- [ ] **Add time-travel section to README**
  - [ ] Explain checkpoint history
  - [ ] Show commands: history, show-checkpoint, fork
  - [ ] Use case: Debugging, exploration
  - **File:** `README.md`

- [ ] **Create time-travel examples**
  - [ ] Example: View conversation history
  - [ ] Example: Fork from earlier point
  - [ ] Example: Compare different execution paths
  - **File:** `examples/time_travel_examples.py` (NEW)

**Acceptance Criteria:**

- [ ] Three commands implemented: history, show-checkpoint, fork
- [ ] Commands work with existing checkpointer
- [ ] Documented in README with examples
- [ ] User-friendly output formatting

**References:**

- `docs/recommendations/SUMMARY.md` (Time-Travel section)
- `docs/recommendations/11-time-travel.md`

---

## Completed Work (Reference)

### Phase 0: Core Implementation ✅ COMPLETE

**Completed:** All phases from original development (Phases 1-5)

- [x] **Phase 1: Foundation**
  - [x] Python 3.11+ with uv package manager
  - [x] Project structure (src/, tests/, docs/)
  - [x] Core modules (config, client, state_schemas)
  - [x] LangGraph v1.0.0 dependencies

- [x] **Phase 2: Tools & Subgraphs**
  - [x] 22 initial tools (address objects, service objects, policies)
  - [x] CRUD subgraph for object management
  - [x] MemorySaver checkpointer for persistence

- [x] **Phase 3: Dual-Mode Graphs**
  - [x] Autonomous graph (ReAct pattern with 33 tools)
  - [x] Deterministic graph (workflow pattern)
  - [x] CLI with typer
  - [x] 6 prebuilt workflows

- [x] **Phase 4: Advanced Features**
  - [x] Commit subgraph with human-in-the-loop
  - [x] Policy tools (security, NAT, PBF)
  - [x] NAT tools
  - [x] Total: 33 tools across all categories

- [x] **Phase 5: Testing & Polish**
  - [x] Pre-commit hooks (black, isort, ruff)
  - [x] pytest configuration
  - [x] Comprehensive documentation (README, ARCHITECTURE, SETUP)
  - [x] 25 LangGraph v1.0.0 recommendation reviews

**Status:** Production-ready core functionality. This TODO adds observability, testing, and enhancements.

---

## Progress Tracking

### Phase 1 Progress (16-24h)

- [ ] 1. Observability & Security (0 / 4.5h)
- [ ] 2. Testing Infrastructure (0 / 10h)
- [ ] 3. Error Handling (0 / 4h)
**Total Phase 1:** 0 / 18.5h

### Phase 2 Progress (12-18h)

- [ ] 4. Store API (0 / 7h)
- [ ] 5. Runtime Context (0 / 3h)
- [ ] 6. Recursion Handling (0 / 2.5h)
- [ ] 7. Deployment Docs (0 / 1.5h)
- [ ] 8. Streaming UX (0 / 2.5h)
**Total Phase 2:** 0 / 16.5h

### Phase 3 Progress (5-9h)

- [ ] 9. Agent Chat UI (0 / 1.5h)
- [ ] 10. Node Caching (0 / 1.5h)
- [ ] 11. Time-Travel CLI (0 / 2.5h)
**Total Phase 3:** 0 / 5.5h

**Grand Total:** 0 / 40.5h (~41 hours median estimate)

---

## Dependencies Graph

```
Phase 1:
  1.1 (env vars) ─→ 1.2 (anonymizers) ─→ 1.3 (metadata)
  2.1 (unit tests) ─→ 2.2 (integration tests)
  1.3 (metadata) ─→ 2.3 (evaluation)

  Independent: 3.1, 3.2, 3.3 (can run in parallel)

Phase 2:
  5 (runtime context) ─→ 6 (recursion handling)
  1.3 (from Phase 1) ─→ 7 (deployment docs)

  Independent: 4, 8 (can run in parallel)

Phase 3:
  All independent (can run in any order or skip entirely)
```

---

## Quick Start Guide

**To begin implementation:**

1. **Start with Phase 1, Task 1.1-1.2 (CRITICAL)**
   - Add LangSmith env vars (30 min)
   - Implement anonymizers (2-3h)
   - **DO NOT enable tracing until anonymizers are complete**

2. **Continue Phase 1 sequentially**
   - Complete observability (1.3)
   - Add unit tests (2.1)
   - Add integration tests (2.2)

3. **Phase 1 can be parallelized:**
   - One developer: Observability (1.1-1.3)
   - Another developer: Testing (2.1-2.2)
   - Another developer: Error handling (3.1-3.3)

4. **Phase 2 after Phase 1 complete**
   - Prioritize: Streaming UX (8) for immediate user benefit
   - Then: Store API (4), Runtime Context (5)

5. **Phase 3 optional**
   - Implement only if time permits
   - Best ROI: Time-travel CLI (11), Agent Chat UI (9)

---

## Notes

- **Security:** Task 1.2 (anonymizers) is CRITICAL before enabling LangSmith
- **Testing:** Tasks 2.1-2.2 provide foundation for confident development
- **UX:** Task 8 (streaming) provides significant perceived performance improvement
- **Flexibility:** Phase 3 tasks are entirely optional based on user needs

**Questions?** See:

- `docs/recommendations/IMPLEMENTATION_PRIORITIES.md` - Detailed rationale
- `docs/recommendations/` - Individual review files (00-24)
- `README.md` - User-facing documentation
- `docs/ARCHITECTURE.md` - Technical architecture

---

**Last Updated:** 2025-01-08
**Total Tasks:** 60+ subtasks across 11 major tasks
**Estimated Completion:** 33-51 hours (4-6 days for 1 developer, 2-3 days for 2 developers)
