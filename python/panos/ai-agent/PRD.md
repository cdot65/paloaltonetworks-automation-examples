# Product Requirements Document: PAN-OS Agent Enhancements

**Project:** PAN-OS Automation AI Agent v1.0.0
**Document Version:** 1.0
**Date:** 2025-01-08
**Status:** Approved for Implementation
**Owner:** Development Team

---

## Executive Summary

### Purpose

This PRD defines requirements for enhancing the PAN-OS automation AI agent from a functional
implementation to a production-ready system. The enhancements address critical gaps in
observability, testing, and resilience identified through a comprehensive review of 25
LangGraph v1.0.0 documentation files.

### Current State

The PAN-OS agent (v0.1.0) is a functional dual-mode AI system with:

- ✅ 33 tools across 6 categories (address objects, service objects, policies, NAT, system)
- ✅ Dual-mode architecture (autonomous ReAct + deterministic workflows)
- ✅ Human-in-the-loop for commit operations
- ✅ Checkpointing for conversation persistence
- ✅ Comprehensive documentation (README, ARCHITECTURE, SETUP)
- ✅ LangGraph v1.0.0 core patterns fully aligned

**Gap Analysis:**

- ❌ No observability (cannot debug in production)
- ❌ No automated testing (regression risk)
- ❌ Limited error handling (timeouts, retries)
- ❌ No long-term memory (each session starts fresh)
- ❌ Limited flexibility (hardcoded model configuration)

### Desired State

Production-ready system with:

- ✅ Full observability via LangSmith (with credential anonymization)
- ✅ Comprehensive test coverage (unit + integration + evaluation)
- ✅ Resilient error handling (timeouts, retries, graceful degradation)
- ✅ Context-aware responses (long-term memory of firewall state)
- ✅ Flexible model selection (Sonnet vs Haiku based on task)
- ✅ Enhanced UX (streaming feedback, time-travel debugging)

### Success Criteria

**Phase 1 (Production Readiness):**

- All sensitive data anonymized in traces (0% credential leakage)
- >80% code coverage on critical paths
- <1% failure rate on transient errors
- 100% of executions traced with metadata

**Phase 2 (Robustness):**

- Context awareness improves response relevance by 30%
- Support 50+ step workflows without failures
- Deployment documentation enables setup in <5 steps

**Phase 3 (Optional):**

- 50% reduction in repeated API calls (caching)
- Time-travel debugging available for power users

### Timeline

- **Phase 1:** 16-24 hours (2-3 days) - CRITICAL
- **Phase 2:** 12-18 hours (1.5-2 days) - HIGH
- **Phase 3:** 5-9 hours (1 day) - LOW
- **Total:** 33-51 hours (4-6 days for 1 developer)

**Target Completion:** 2 weeks from approval

---

## Problem Statement

### Background

The PAN-OS automation agent was developed to streamline firewall management through
conversational AI. After completing core functionality (33 tools, dual-mode architecture, HITL),
a systematic review against LangGraph v1.0.0 documentation revealed production-readiness gaps.

### Problems to Solve

#### 1. Security Risk: Credential Leakage (CRITICAL)

**Problem:**
Enabling LangSmith tracing without anonymization would leak:

- PAN-OS passwords and API keys (LUFRPT... format)
- Anthropic API keys (sk-ant-... format)
- Sensitive firewall configuration data

**Impact:**

- Security breach and compliance violations
- Cannot use observability tools in production
- No visibility into agent behavior or failures

**Current Workaround:**
Tracing disabled entirely (no observability)

---

#### 2. Quality Risk: No Automated Testing (HIGH)

**Problem:**

- Zero unit tests for node functions and tools
- Zero integration tests for end-to-end flows
- No LLM evaluation framework
- Manual testing only (slow, error-prone)

**Impact:**

- Regressions can slip into production undetected
- Cannot confidently deploy changes
- Debugging requires hours of manual reproduction
- No metrics on agent performance (tool selection accuracy, response quality)

**Current Workaround:**
Extensive manual testing before each deployment

---

#### 3. Resilience Gap: Inadequate Error Handling (MEDIUM-HIGH)

**Problem:**

- No timeout handling (operations can hang indefinitely)
- No retry policies (transient network errors cause failures)
- No graceful degradation (long workflows hit recursion limits)
- Unclear resume strategies after failures

**Impact:**

- Poor user experience (45s commits appear hung)
- Transient failures treated as permanent
- Complex workflows fail unexpectedly
- Users don't know how to recover from failures

**Current Workaround:**
Users manually retry entire operations

---

#### 4. Context Gap: No Long-Term Memory (MEDIUM)

**Problem:**

- Each session starts with zero context
- Agent cannot remember previous firewall configurations
- Cannot learn from workflow execution patterns
- Repeats same questions across sessions

**Impact:**

- Inefficient conversations (repeated context gathering)
- Cannot provide context-aware recommendations
- No workflow execution history for auditing

**Current Workaround:**
Users provide context in every prompt

---

#### 5. Flexibility Gap: Hardcoded Configuration (MEDIUM)

**Problem:**

- LLM model hardcoded (`claude-3-5-sonnet-20241022`)
- Temperature hardcoded (0.0)
- Cannot switch models per task (Haiku for simple, Sonnet for complex)
- Difficult to test with mock LLM

**Impact:**

- Suboptimal cost/performance tradeoffs
- Cannot experiment with different models
- Integration testing requires real LLM API calls
- Expensive to run simple queries

**Current Workaround:**
All queries use expensive Sonnet model

---

### Root Causes

1. **Rapid prototyping focus:** Core functionality prioritized over production infrastructure
2. **Documentation gap:** LangGraph v1.0.0 features not fully explored until systematic review
3. **Resource constraints:** Single developer focused on feature completeness
4. **Knowledge gap:** Advanced patterns (anonymizers, Store API, RetryPolicy) not initially known

---

## Objectives

### Primary Objectives

1. **Security: Eliminate Credential Leakage Risk**
   - Implement anonymizers for all sensitive data patterns
   - Enable LangSmith tracing safely
   - Validate zero credential leakage in production traces
   - **Success Metric:** 100% of sensitive patterns masked

2. **Quality: Establish Automated Testing**
   - Build unit test suite (nodes, tools, routing)
   - Build integration test suite (end-to-end flows)
   - Establish LLM evaluation framework
   - **Success Metric:** >80% code coverage, all tests pass in CI

3. **Reliability: Improve Error Handling**
   - Implement timeout handling
   - Add retry policies for transient failures
   - Support graceful degradation for long workflows
   - **Success Metric:** <1% failure rate on transient errors

### Secondary Objectives

1. **Context: Add Long-Term Memory**
   - Implement Store API for firewall configuration history
   - Remember workflow execution patterns
   - Provide context-aware responses
   - **Success Metric:** 30% improvement in response relevance

2. **Flexibility: Enable Runtime Configuration**
   - Support dynamic model selection (Sonnet, Haiku)
   - Allow temperature tuning per invocation
   - Enable dependency injection for testing
   - **Success Metric:** 50% cost reduction on simple queries (Haiku)

3. **UX: Enhance User Experience**
   - Implement streaming for real-time feedback
   - Document deployment process
   - Add time-travel debugging for power users
   - **Success Metric:** Perceived performance improvement, <5 step deployment

### Non-Objectives (Out of Scope)

- ❌ Multi-tenant architecture (single-user focus)
- ❌ Web UI development (CLI + Agent Chat UI sufficient)
- ❌ Batch multi-host operations (single firewall per session)
- ❌ Advanced caching (most operations are non-cacheable writes)
- ❌ Performance optimization beyond basic caching
- ❌ Alternative LLM providers (Anthropic Claude only)

---

## User Personas

### Persona 1: Alex - Network Engineer (Primary)

**Role:** Senior Network Engineer at mid-sized enterprise
**Experience:** 8 years networking, 2 years PAN-OS
**Technical Level:** Intermediate Python, expert PAN-OS

**Goals:**

- Automate repetitive firewall configuration tasks
- Reduce manual errors in policy management
- Quickly respond to access requests
- Maintain audit trail of changes

**Pain Points:**

- PAN-OS XML API is complex and unintuitive
- Manual configuration is time-consuming and error-prone
- Difficult to maintain consistency across environments
- Hard to remember exact syntax for every operation

**Use Cases:**

1. **Ad-hoc Operations:** "Create address object prod-db-01 with IP 10.1.2.50"
2. **Policy Management:** "Show all security policies with source zone 'untrust'"
3. **Access Requests:** "Set up DMZ access for new web application on ports 80, 443"

**Requirements:**

- Fast response times (<5s for simple operations)
- Clear error messages with actionable guidance
- Ability to resume from failures
- Conversational interface (no XML/API knowledge needed)

---

### Persona 2: Jordan - DevOps Engineer (Primary)

**Role:** DevOps Team Lead at software company
**Experience:** 10 years DevOps, 1 year PAN-OS
**Technical Level:** Expert Python/CI/CD, beginner PAN-OS

**Goals:**

- Integrate firewall changes into CI/CD pipelines
- Implement infrastructure as code for security policies
- Automate security policy updates on deployments
- Maintain repeatability and auditability

**Pain Points:**

- Firewall changes are manual and slow down deployments
- Difficult to version control firewall configurations
- No way to test firewall changes before production
- Lack of observability into automation failures

**Use Cases:**

1. **CI/CD Integration:** Run deterministic workflows in GitHub Actions
2. **Infrastructure as Code:** Define security policies in YAML, apply via agent
3. **Deployment Automation:** "Update security policy allow-app-01 with new backend IPs"
4. **Compliance Reporting:** Query LangSmith traces for audit logs

**Requirements:**

- Deterministic, repeatable workflows
- Full observability (traces, logs, metrics)
- API access (REST, Python SDK)
- Non-interactive mode (no HITL in CI/CD)
- Comprehensive error handling and logging

---

### Persona 3: Sam - Security Analyst (Secondary)

**Role:** Security Operations Analyst
**Experience:** 5 years security, 3 years PAN-OS
**Technical Level:** Basic Python, expert security

**Goals:**

- Review all firewall changes for compliance
- Investigate security incidents quickly
- Approve critical policy changes
- Maintain security posture

**Pain Points:**

- No visibility into automated changes
- Difficult to review agent decision-making
- Need approval gate for sensitive operations
- Hard to investigate "why did the agent do X?"

**Use Cases:**

1. **Change Review:** Review all agent-made changes in LangSmith traces
2. **Approval Workflow:** Approve commits via human-in-the-loop
3. **Incident Investigation:** "Show all security policy changes in last 7 days"
4. **Audit Trails:** Export LangSmith traces for compliance reports

**Requirements:**

- Full trace visibility (anonymized credentials)
- Human-in-the-loop for commits
- Clear explanations of agent reasoning
- Ability to rollback changes
- Compliance-friendly audit logs

---

### Persona 4: Morgan - Python Developer (Secondary)

**Role:** Open Source Contributor / Internal Developer
**Experience:** 6 years Python, 0 years PAN-OS
**Technical Level:** Expert Python, beginner networking

**Goals:**

- Extend agent with new tools and workflows
- Contribute to open source project
- Customize agent for organization-specific needs
- Learn LangGraph development

**Pain Points:**

- Need to understand complex graph architecture
- Difficult to test new tools without PAN-OS instance
- Unclear how to add new subgraphs
- No clear contribution guidelines for testing

**Use Cases:**

1. **Tool Development:** Add support for new PAN-OS object types (zones, interfaces)
2. **Workflow Creation:** Build organization-specific workflows
3. **Testing:** Write unit tests for new tools
4. **Documentation:** Improve developer documentation

**Requirements:**

- Clear architecture documentation
- Comprehensive test suite as examples
- Mocking/testing patterns for PAN-OS API
- Developer setup guide
- Code contribution guidelines

---

## Requirements

### Functional Requirements

#### FR1: Anonymization (CRITICAL)

**Priority:** P0 (Production Blocker)

**Requirements:**

- **FR1.1:** System SHALL mask all PAN-OS API keys (LUFRPT... format) in traces
- **FR1.2:** System SHALL mask all Anthropic API keys (sk-ant-... format) in traces
- **FR1.3:** System SHALL mask all password fields (password=, passwd=, pwd=) in traces
- **FR1.4:** System SHALL mask XML password elements (`<password>...</password>`) in traces
- **FR1.5:** Anonymization SHALL NOT produce false positives (mask legitimate data)
- **FR1.6:** Anonymization SHALL be applied before traces are sent to LangSmith

**Acceptance Criteria:**

- Manual review of 10 production traces shows zero credential leakage
- Unit tests verify all patterns detected correctly
- Integration test confirms masked values in LangSmith UI

**Reference:** Task 1.2 in TODO.md

---

#### FR2: Observability (HIGH)

**Priority:** P0 (Production Blocker)

**Requirements:**

- **FR2.1:** System SHALL send traces to LangSmith when LANGSMITH_TRACING=true
- **FR2.2:** System SHALL tag all traces with: agent name, mode, version
- **FR2.3:** System SHALL include metadata: thread_id, firewall_host, timestamp, mode-specific data
- **FR2.4:** System SHALL work without LangSmith (graceful degradation when tracing disabled)
- **FR2.5:** System SHALL log errors if LangSmith connection fails (non-blocking)

**Acceptance Criteria:**

- Traces visible in LangSmith UI with correct tags
- Metadata enables filtering by mode, host, version
- Agent works without LangSmith configured

**Reference:** Tasks 1.1, 1.3 in TODO.md

---

#### FR3: Testing (HIGH)

**Priority:** P0 (Production Blocker)

**Requirements:**

- **FR3.1:** System SHALL have unit tests for all node functions
- **FR3.2:** System SHALL have unit tests for all routing functions
- **FR3.3:** System SHALL have unit tests for representative tools from each category
- **FR3.4:** System SHALL have integration tests for autonomous graph end-to-end flows
- **FR3.5:** System SHALL have integration tests for deterministic graph end-to-end flows
- **FR3.6:** System SHALL have integration tests for checkpointing and resume
- **FR3.7:** System SHALL have LangSmith evaluation dataset with 10+ examples
- **FR3.8:** Unit tests SHALL use mocks (no real PAN-OS API calls)
- **FR3.9:** Integration tests SHALL use mocks (no real PAN-OS API calls)

**Acceptance Criteria:**

- All tests pass: `pytest tests/ -v`
- Code coverage >80% on src/autonomous_graph.py, src/deterministic_graph.py
- Tests run in <30 seconds
- CI integration (tests run on every commit)

**Reference:** Tasks 2.1, 2.2, 2.3 in TODO.md

---

#### FR4: Error Handling (MEDIUM-HIGH)

**Priority:** P1 (High Value)

**Requirements:**

- **FR4.1:** System SHALL timeout operations after configured limit (300s autonomous,
  600s deterministic)
- **FR4.2:** System SHALL retry PAN-OS API operations up to 3 times on transient failures
- **FR4.3:** System SHALL use exponential backoff for retries (2s, 4s, 8s)
- **FR4.4:** System SHALL log all retry attempts with context
- **FR4.5:** System SHALL provide user-friendly error messages on final failure
- **FR4.6:** System SHALL document resume strategies for users

**Acceptance Criteria:**

- Operations timeout as configured
- Transient failures retry automatically
- Final failures provide clear guidance
- Documentation explains recovery process

**Reference:** Tasks 3.1, 3.2, 3.3 in TODO.md

---

#### FR5: Long-Term Memory (MEDIUM)

**Priority:** P2 (Enhancement)

**Requirements:**

- **FR5.1:** System SHALL store firewall configuration state in Store API
- **FR5.2:** System SHALL store workflow execution history in Store API
- **FR5.3:** System SHALL retrieve previous context before operations
- **FR5.4:** System SHALL include memory context in agent prompts
- **FR5.5:** System SHALL use namespace: ("firewall_configs", hostname) for firewall state
- **FR5.6:** System SHALL use namespace: ("workflow_history", workflow_name) for workflows
- **FR5.7:** Memory SHALL persist across sessions (until explicitly cleared)

**Acceptance Criteria:**

- Agent references previous operations in responses
- Workflow history tracks all executions
- Memory persists across restarts (if using persistent store)
- Documentation explains memory schema

**Reference:** Task 4 in TODO.md

---

#### FR6: Runtime Configuration (MEDIUM)

**Priority:** P2 (Enhancement)

**Requirements:**

- **FR6.1:** System SHALL support runtime model selection (Sonnet, Haiku, Opus)
- **FR6.2:** System SHALL support runtime temperature configuration (0.0-1.0)
- **FR6.3:** System SHALL support runtime max_tokens configuration
- **FR6.4:** CLI SHALL provide `--model` flag with choices: sonnet, haiku, opus
- **FR6.5:** CLI SHALL provide `--temperature` flag with range 0.0-1.0
- **FR6.6:** System SHALL use defaults when runtime config not provided
- **FR6.7:** Runtime context SHALL NOT pollute state (separate from state)

**Acceptance Criteria:**

- Model selection works: `--model haiku` uses claude-3-5-haiku
- Temperature works: `--temperature 0.7` sets temp to 0.7
- Defaults work without flags
- Documentation explains cost/speed tradeoffs

**Reference:** Task 5 in TODO.md

---

#### FR7: Streaming (MEDIUM-HIGH)

**Priority:** P1 (High Value for UX)

**Requirements:**

- **FR7.1:** System SHALL stream node outputs in real-time (default behavior)
- **FR7.2:** System SHALL display progress indicators (🔄 Agent thinking, 🔧 Executing tools,
  ✅ Complete)
- **FR7.3:** Deterministic mode SHALL display step-by-step progress (Step 1/5: ...)
- **FR7.4:** CLI SHALL provide `--no-stream` flag for automation (use .invoke())
- **FR7.5:** Streaming SHALL flush output immediately (no buffering)

**Acceptance Criteria:**

- Real-time feedback visible during execution
- User sees what's happening at each step
- `--no-stream` works for CI/CD (no ANSI codes)
- Documentation shows streaming examples

**Reference:** Task 8 in TODO.md

---

#### FR8: Recursion Handling (MEDIUM)

**Priority:** P2 (Enhancement)

**Requirements:**

- **FR8.1:** System SHALL check recursion limit at each workflow step
- **FR8.2:** System SHALL warn at 50% of recursion limit
- **FR8.3:** System SHALL stop gracefully at 80% of recursion limit
- **FR8.4:** System SHALL return partial results with clear explanation
- **FR8.5:** Autonomous mode SHALL use default limit (25 steps)
- **FR8.6:** Deterministic mode SHALL use increased limit (50 steps)
- **FR8.7:** Users SHALL be able to override via `--recursion-limit` flag

**Acceptance Criteria:**

- Long workflows (30 steps) stop gracefully at 40 steps (80% of 50)
- Clear message explains partial completion
- Partial progress saved in checkpoint
- Documentation explains limits

**Reference:** Task 6 in TODO.md

---

#### FR9: Deployment (MEDIUM)

**Priority:** P2 (Enhancement)

**Requirements:**

- **FR9.1:** Documentation SHALL provide step-by-step deployment guide
- **FR9.2:** Documentation SHALL show LangSmith deployment process
- **FR9.3:** Documentation SHALL include Python SDK examples
- **FR9.4:** Documentation SHALL include REST API examples (curl)
- **FR9.5:** Documentation SHALL include deployment checklist
- **FR9.6:** Examples SHALL demonstrate: create thread, run agent, stream responses

**Acceptance Criteria:**

- Deployment guide enables setup in <5 steps
- API examples run successfully against deployed agent
- Checklist ensures production readiness
- REST API documented with working curl commands

**Reference:** Task 7 in TODO.md

---

### Non-Functional Requirements

#### NFR1: Performance

- **NFR1.1:** Simple queries SHALL respond in <5 seconds (P99)
- **NFR1.2:** Complex workflows SHALL complete in <60 seconds per step (P99)
- **NFR1.3:** Test suite SHALL complete in <30 seconds
- **NFR1.4:** Streaming SHALL introduce <100ms latency overhead

#### NFR2: Reliability

- **NFR2.1:** System SHALL achieve <1% failure rate on transient errors (with retries)
- **NFR2.2:** System SHALL achieve 99% uptime in production
- **NFR2.3:** System SHALL recover automatically from network failures (via retries)
- **NFR2.4:** System SHALL preserve state across crashes (via checkpointing)

#### NFR3: Security

- **NFR3.1:** System SHALL NOT log credentials in plaintext
- **NFR3.2:** System SHALL mask 100% of sensitive data patterns in traces
- **NFR3.3:** System SHALL use secure connections (HTTPS) for LangSmith
- **NFR3.4:** System SHALL validate all user inputs (prevent injection attacks)

#### NFR4: Usability

- **NFR4.1:** Error messages SHALL be actionable (explain what to do next)
- **NFR4.2:** Streaming output SHALL clearly indicate progress
- **NFR4.3:** Documentation SHALL enable new users to deploy in <1 hour
- **NFR4.4:** CLI help SHALL be comprehensive (`--help` for all commands)

#### NFR5: Maintainability

- **NFR5.1:** Code coverage SHALL be >80% on critical paths
- **NFR5.2:** All functions SHALL have docstrings
- **NFR5.3:** Architecture documentation SHALL be up-to-date
- **NFR5.4:** Contribution guidelines SHALL exist for developers

#### NFR6: Scalability

- **NFR6.1:** System SHALL support conversations with 100+ messages
- **NFR6.2:** System SHALL support workflows with 50+ steps
- **NFR6.3:** System SHALL support 10+ concurrent sessions (deployed)
- **NFR6.4:** System SHALL handle 1000+ tools calls per day

---

## Success Metrics & KPIs

### Phase 1: Production Readiness

**Security Metrics:**

- **Credential Leakage Rate:** 0% (target: 0%, measured by manual trace review)
- **Anonymization Coverage:** 100% of sensitive patterns masked (target: 100%)
- **False Positive Rate:** <1% (legitimate data masked incorrectly)

**Quality Metrics:**

- **Code Coverage:** >80% on critical paths (target: 80%, measured by pytest-cov)
- **Test Pass Rate:** 100% (all tests pass on main branch)
- **Test Execution Time:** <30s for full suite (target: <30s)
- **Regression Rate:** <2% of commits introduce bugs (target: <2%, measured by test failures)

**Reliability Metrics:**

- **Transient Failure Rate:** <1% after retries (target: <1%, measured by logs)
- **Timeout Rate:** <0.5% of operations (target: <0.5%)
- **Retry Success Rate:** >95% of transient failures succeed within 3 attempts (target: >95%)

**Observability Metrics:**

- **Trace Coverage:** 100% of executions traced (target: 100%, when tracing enabled)
- **Metadata Completeness:** 100% of traces include all required metadata (target: 100%)
- **LangSmith Uptime:** >99% (external dependency)

---

### Phase 2: Robustness Enhancements

**Context Awareness Metrics:**

- **Memory Hit Rate:** >90% of operations find relevant context (target: >90%)
- **Response Relevance:** 30% improvement (measured by user feedback or LLM evaluation)
- **Context Usage Rate:** >70% of agent responses reference memory (target: >70%)

**Flexibility Metrics:**

- **Model Selection Rate:** >30% of operations use Haiku (cheaper model) (target: >30%)
- **Cost Reduction:** 50% reduction on simple queries (target: 50%, measured by token usage)
- **Temperature Usage:** >10% of operations use non-zero temperature (target: >10%)

**Scalability Metrics:**

- **Max Workflow Length:** Support 50 steps without recursion errors (target: 50)
- **Recursion Limit Utilization:** <5% of workflows hit recursion limit (target: <5%)
- **Long Workflow Success Rate:** >98% for workflows with 20+ steps (target: >98%)

**Deployment Metrics:**

- **Time to Deploy:** <5 steps, <15 minutes (target: <15 min, measured by new user)
- **Deployment Success Rate:** >95% first-time success (target: >95%)
- **API Example Success Rate:** 100% of examples work (target: 100%)

---

### Phase 3: Optional Enhancements

**Performance Metrics:**

- **Cache Hit Rate:** >40% for read operations (target: >40%, if caching implemented)
- **API Call Reduction:** 50% reduction in repeated reads (target: 50%)
- **Response Time Improvement:** 30% faster for cached operations (target: 30%)

**Power User Metrics:**

- **Time-Travel Usage:** >10% of power users use history/fork commands (target: >10%)
- **Agent Chat UI Adoption:** >20% of developers use UI for debugging (target: >20%)
- **Advanced Feature Discovery:** >50% of users aware of time-travel (target: >50%, via docs)

---

### Overall Product Health

**User Satisfaction:**

- **NPS (Net Promoter Score):** >50 (measured by survey)
- **Feature Request Volume:** Decreasing (indicates core needs met)
- **Bug Report Volume:** <5 per month (high quality)

**Operational Health:**

- **Mean Time to Detect (MTTD):** <5 minutes (observability enables fast detection)
- **Mean Time to Repair (MTTR):** <30 minutes (time-travel enables fast debugging)
- **Incident Rate:** <1 per week

---

## Technical Architecture

### System Architecture

```texttexttexttexttexttexttexttexttexttextpythontext
┌─────────────────────────────────────────────────────────────┐
│                     PAN-OS Agent v1.0.0                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────┐    ┌────────────────┐    ┌────────────┐  │
│  │   CLI Layer   │───▶│  Graph Layer   │───▶│ Tool Layer │  │
│  └───────────────┘    └────────────────┘    └────────────┘  │
│         │                      │                     │        │
│         │                      │                     │        │
│    ┌────▼──────┐          ┌───▼────┐          ┌────▼─────┐  │
│    │ Streaming │          │ Store  │          │  PAN-OS  │  │
│    │  Output   │          │  API   │          │  Client  │  │
│    └───────────┘          └────────┘          └──────────┘  │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                   Infrastructure Layer                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Checkpointer │  │  Anonymizer  │  │ Retry Policy │      │
│  │ (MemorySaver)│  │  (LangSmith) │  │  (Pregel)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │      External Services          │
         ├────────────────────────────────┤
         │ • LangSmith (Observability)    │
         │ • Anthropic (Claude LLM)       │
         │ • PAN-OS Firewall (API)        │
         └────────────────────────────────┘
```

---

### Component Design

#### 1. Anonymizer Component

**Location:** `src/core/anonymizers.py`

**Purpose:** Mask sensitive data before sending to LangSmith

**Design:**

```python
# Pattern-based anonymization using langchain_core
anonymizer = create_anonymizer([
    {"pattern": r"LUFRPT[A-Za-z0-9+/=]{40,}", "replace": "<panos-api-key>"},
    {"pattern": r"sk-ant-[A-Za-z0-9-_]{40,}", "replace": "<anthropic-api-key>"},
    {"pattern": r"(password|passwd|pwd)['\"]?\s*[:=]\s*['\"]?[^\s'\"]+",
     "replace": r"\1: <password>"},
    {"pattern": r"<password>.*?</password>", "replace": "<password><redacted></password>"},
])

# Integrated into LangSmith tracer
tracer_client = Client(anonymizer=anonymizer)
tracer = LangChainTracer(client=tracer_client)
```

**Key Decisions:**

- Use regex patterns (fast, deterministic)
- Apply client-side (data never leaves in cleartext)
- Comprehensive patterns (API keys, passwords, XML)
- Testable (unit tests verify each pattern)

**References:**

- `docs/recommendations/19-observability.md` (lines 78-145)

---

#### 2. Store API Integration

**Location:** `src/core/memory_store.py`

**Purpose:** Long-term memory across sessions

**Design:**

```python
from langgraph.store.memory import InMemoryStore

# Singleton store
_store = None

def get_store() -> InMemoryStore:
    global _store
    if _store is None:
        _store = InMemoryStore()
    return _store

# Namespace schema:
# ("firewall_configs", hostname) → firewall state
# ("workflow_history", workflow_name) → execution history

# Helper functions:
async def store_firewall_config(hostname: str, config_type: str, data: dict):
    await store.put(
        namespace=("firewall_configs", hostname),
        key={"config_type": config_type},
        value=data
    )

async def retrieve_firewall_config(hostname: str, config_type: str) -> dict | None:
    results = await store.search(
        namespace_prefix=("firewall_configs", hostname),
    )
    return next((r.value for r in results if r.key["config_type"] == config_type), None)
```

**Key Decisions:**

- InMemoryStore for simplicity (can upgrade to persistent later)
- Namespace per firewall (isolation)
- Helper functions (consistent interface)
- Async API (future-proof for persistent stores)

**References:**

- `docs/recommendations/12-add-memory.md` (lines 79-154)

---

#### 3. Runtime Context

**Location:** `src/core/config.py`

**Purpose:** Dynamic model/temperature selection

**Design:**

```python
from dataclasses import dataclass
from langgraph.runtime import Runtime

@dataclass
class AgentContext:
    """Runtime context for agent graphs."""
    model_name: str = "claude-3-5-sonnet-20241022"
    temperature: float = 0.0
    max_tokens: int = 4096

# Usage in nodes:
def call_agent(state: AutonomousState, runtime: Runtime[AgentContext]) -> dict:
    llm = ChatAnthropic(
        model=runtime.context.model_name,
        temperature=runtime.context.temperature,
        max_tokens=runtime.context.max_tokens,
    )
    # ...

# CLI invocation:
graph.invoke(
    input,
    config={...},
    context={"model_name": "claude-3-5-haiku-20241022"}
)
```

**Key Decisions:**

- Dataclass (simple, typed)
- Not part of state (doesn't pollute checkpoints)
- CLI flags map to context
- Defaults work without context

**References:**

- `docs/recommendations/20-graph-api.md` (lines 99-156)

---

#### 4. Retry Policies

**Location:** `src/core/retry_policies.py`

**Purpose:** Handle transient PAN-OS API failures

**Design:**

```python
from langgraph.pregel import RetryPolicy

PANOS_RETRY_POLICY = RetryPolicy(
    max_attempts=3,
    retry_on=(PanDeviceError, ConnectionError, TimeoutError),
    backoff_factor=2.0,  # 2s, 4s, 8s
)

# Applied to nodes:
workflow.add_node("tools", tool_node, retry=PANOS_RETRY_POLICY)
```

**Key Decisions:**

- Exponential backoff (avoid thundering herd)
- Specific exceptions (don't retry permanent failures)
- 3 attempts (balance between resilience and latency)
- Applied per-node (granular control)

**References:**

- `docs/recommendations/08-durable-execution.md` (lines 108-155)
- `docs/recommendations/21-use-the-graph-api.md` (lines 189-225)

---

#### 5. Streaming Output

**Location:** `src/cli/commands.py`

**Purpose:** Real-time feedback to users

**Design:**

```python
# Replace .invoke() with .stream()
for chunk in graph.stream(input, config, stream_mode="updates"):
    node_name = chunk.keys()[0]
    output = chunk[node_name]

    # Display progress
    if node_name == "agent":
        print("🤖 Agent thinking...")
    elif node_name == "tools":
        print("🔧 Executing tools...")

    # Display output
    print(output)
```

**Key Decisions:**

- stream_mode="updates" (one update per node)
- Progress indicators (visual feedback)
- `--no-stream` flag (automation use case)
- Color-coded output (success/error)

**References:**

- `docs/recommendations/SUMMARY.md` (Streaming UX)
- `docs/recommendations/09-streaming.md`

---

### Data Flow

#### Autonomous Mode (with enhancements)

```text
User Input
    │
    ▼
┌───────────────┐
│  CLI Parser   │ (--model, --temperature)
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Runtime       │ (model_name, temperature)
│ Context       │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Autonomous    │
│ Graph         │ ◀──── Store API (retrieve context)
└───────┬───────┘
        │
        ├─▶ Agent Node ──▶ Claude LLM (with runtime context)
        │
        ├─▶ Tool Node ──▶ PAN-OS API (with retry policy)
        │       │
        │       └─────▶ Store API (save results)
        │
        ├─▶ Checkpointer (save state)
        │
        └─▶ LangSmith (anonymized trace)
             │
             ▼
        Streaming Output
             │
             ▼
          User
```

---

### Testing Strategy

#### Unit Tests (4-6 hours)

**Scope:**

- Node functions (call_agent, route_after_agent, etc.)
- Routing functions (all conditional edges)
- Tool invocations (representative tools from each category)
- Subgraph nodes (CRUD, commit, deterministic workflow)

**Approach:**

- Mock external dependencies (LLM, PAN-OS API)
- Test state transformations (input state → output state)
- Test routing logic (state → next node)
- Test error handling (invalid inputs → error messages)

**Tools:**

- pytest (test runner)
- pytest-mock (mocking)
- pytest-cov (coverage)

**Coverage Target:** >80% on src/autonomous_graph.py, src/deterministic_graph.py

---

#### Integration Tests (3-4 hours)

**Scope:**

- End-to-end flows for autonomous graph
- End-to-end flows for deterministic graph
- Checkpointing and resume
- Subgraph invocations
- State management

**Approach:**

- Mock PAN-OS API at client level (global fixture)
- Use real graph instances (compiled)
- Test with real thread_ids (real checkpointing)
- Verify state updates, message accumulation, tool execution

**Tools:**

- pytest (test runner)
- pytest-mock (mocking)
- Fixtures for graphs, thread_ids

**Execution Target:** <30 seconds for full suite

---

#### LangSmith Evaluation (1-2 hours)

**Scope:**

- Representative examples (10-15 examples)
- Coverage: simple queries, CRUD ops, workflows, errors
- Metrics: tool selection accuracy, response quality, token efficiency

**Approach:**

- Create evaluation dataset in LangSmith UI
- Run agent on each example
- Collect metrics (success rate, token usage, latency)
- Set up regression alerts (>10% degradation triggers alert)

**Tools:**

- LangSmith evaluation framework
- Python evaluation script

**Metrics:**

- Success Rate: >90%
- Token Efficiency: <5000 tokens per operation
- Latency: <5s per operation

---

### Deployment Architecture

```text
GitHub Repository
      │
      ▼
LangGraph Deploy Command
      │
      ▼
LangSmith Cloud
      │
      ├─▶ Graph Runtime (handles requests)
      │
      ├─▶ Checkpointer (PostgreSQL)
      │
      ├─▶ Store (persistent)
      │
      └─▶ Observability (traces, metrics)
            │
            ▼
┌───────────────────────────────────┐
│   Client Access Methods           │
├───────────────────────────────────┤
│ • Python SDK (langgraph-sdk)     │
│ • REST API (HTTPS)                │
│ • Agent Chat UI (web interface)   │
└───────────────────────────────────┘
```

**Key Decisions:**

- GitHub as source of truth
- LangSmith handles scaling, persistence
- Multiple access methods (SDK, REST, UI)
- Observability built-in (traces, metrics)

---

## Risks & Mitigation

### Critical Risks

#### Risk 1: Credential Leakage in LangSmith Traces

**Probability:** HIGH (if tracing enabled before anonymizers)
**Impact:** CRITICAL (security breach, compliance violation)

**Root Cause:**

- LangSmith traces entire LLM conversation
- PAN-OS passwords and API keys in messages
- Anthropic API keys in configuration

**Mitigation Strategy:**

1. **Prevent:** Implement anonymizers BEFORE enabling tracing (Task 1.2 before 1.3)
2. **Detect:** Manual review of first 10 production traces
3. **Validate:** Unit tests verify all patterns masked
4. **Recover:** If leak detected, rotate all credentials immediately

**Owner:** Development Team
**Status:** Mitigated by implementation order (1.2 → 1.3)

---

#### Risk 2: Regressions Without Automated Testing

**Probability:** MEDIUM (complex graph logic)
**Impact:** HIGH (bugs in production, user trust loss)

**Root Cause:**

- No automated tests currently
- Manual testing is slow and incomplete
- Complex state management easy to break

**Mitigation Strategy:**

1. **Prevent:** Build comprehensive test suite (Tasks 2.1, 2.2)
2. **Detect:** CI runs tests on every commit
3. **Validate:** Code coverage >80% enforced
4. **Recover:** Rollback to previous version if regression detected

**Owner:** Development Team
**Status:** Mitigated by Phase 1 priority (testing is P0)

---

### High Risks

#### Risk 3: Long Operations Timeout Without Feedback

**Probability:** MEDIUM (commit operations take 45s)
**Impact:** MEDIUM (poor UX, user confusion)

**Root Cause:**

- Blocking .invoke() provides no intermediate feedback
- Commits take 45s (push + commit)
- Users think system is hung

**Mitigation Strategy:**

1. **Prevent:** Implement streaming (Task 8)
2. **Detect:** Add timeout handling (Task 3.1)
3. **Communicate:** Show progress indicators
4. **Recover:** Graceful timeout with clear message

**Owner:** Development Team
**Status:** Mitigated by streaming (high priority in Phase 2)

---

#### Risk 4: Memory Growth in Long-Running Sessions

**Probability:** LOW (InMemoryStore, MemorySaver)
**Impact:** MEDIUM (performance degradation)

**Root Cause:**

- InMemoryStore keeps all data in RAM
- MemorySaver keeps all checkpoints in RAM
- Long sessions accumulate large state

**Mitigation Strategy:**

1. **Prevent:** Use SqliteSaver for deployed agents (persistent, bounded)
2. **Monitor:** Track memory usage in production
3. **Limit:** Implement TTL for old checkpoints (prune >7 days)
4. **Document:** Recommend new thread_id for new conversations

**Owner:** Operations Team
**Status:** Low risk (InMemoryStore sufficient for MVP, can upgrade)

---

### Medium Risks

#### Risk 5: Complex Workflows Hit Recursion Limits

**Probability:** LOW (most workflows <25 steps)
**Impact:** MEDIUM (workflow failures, user confusion)

**Root Cause:**

- LangGraph default recursion limit is 25 steps
- Some workflows may exceed (complex network segmentation)
- Hard failures with GraphRecursionError

**Mitigation Strategy:**

1. **Prevent:** Implement recursion handling (Task 6)
2. **Detect:** Warn at 50% of limit
3. **Graceful:** Stop at 80% with partial results
4. **Configure:** Allow users to increase limit

**Owner:** Development Team
**Status:** Mitigated by Task 6 (recursion handling)

---

### Low Risks

#### Risk 6: PAN-OS API Changes Break Tools

**Probability:** LOW (stable XML API)
**Impact:** MEDIUM (tool failures)

**Mitigation:**

- Comprehensive test suite catches API changes
- Version pin pan-os-python library
- Monitor for deprecation warnings

---

#### Risk 7: LangSmith Service Outage

**Probability:** LOW (99% uptime SLA)
**Impact:** LOW (observability unavailable, agent still works)

**Mitigation:**

- Agent works without LangSmith (graceful degradation)
- Local logging continues
- Retry LangSmith connection on transient failures

---

## Timeline & Milestones

### Phase 1: Production Readiness (16-24 hours)

**Target:** Week 1
**Priority:** CRITICAL (production blockers)

| Milestone | Tasks | Hours | Completion Criteria |
|-----------|-------|-------|---------------------|
| **M1.1: Observability** | 1.1, 1.2, 1.3 | 4-5h | LangSmith tracing enabled with anonymization |
| **M1.2: Testing** | 2.1, 2.2, 2.3 | 8-12h | >80% coverage, all tests pass |
| **M1.3: Error Handling** | 3.1, 3.2, 3.3 | 4-6h | Timeouts, retries, resume docs |

**Dependencies:**

- 1.1 → 1.2 → 1.3 (sequential)
- 2.1 → 2.2 (sequential)
- 1.3 → 2.3 (sequential)
- Tasks 3.1-3.3 independent (parallel)

**Deliverables:**

- Anonymizers implemented and tested
- LangSmith tracing enabled
- Unit + integration test suites
- Retry policies applied
- Timeout handling implemented

**Success Criteria:**

- Zero credential leakage (manual trace review)
- All tests pass
- <1% transient failure rate

---

### Phase 2: Robustness Enhancements (12-18 hours)

**Target:** Week 2
**Priority:** HIGH (valuable improvements)

| Milestone | Tasks | Hours | Completion Criteria |
|-----------|-------|-------|---------------------|
| **M2.1: Context** | 4, 5 | 8-12h | Store API + runtime context implemented |
| **M2.2: Resilience** | 6, 8 | 4-6h | Recursion handling + streaming |
| **M2.3: Deployment** | 7 | 1-2h | Deployment docs + API examples |

**Dependencies:**

- Task 4, 5 independent (parallel)
- Task 5 → 6 (sequential)
- Task 7 requires Phase 1 complete
- Task 8 independent (parallel)

**Deliverables:**

- Store API with firewall/workflow memory
- Runtime context for model selection
- Recursion limit handling
- Streaming UX
- Deployment documentation + examples

**Success Criteria:**

- Memory context improves response relevance (30%)
- Support 50+ step workflows
- Deployment in <5 steps

---

### Phase 3: Optional Enhancements (5-9 hours)

**Target:** Week 2 (if time permits)
**Priority:** LOW (nice-to-have)

| Milestone | Tasks | Hours | Completion Criteria |
|-----------|-------|-------|---------------------|
| **M3.1: Power Features** | 9, 10, 11 | 5-9h | Agent Chat UI docs, caching (if needed), |
|                          |           |      | time-travel CLI |

**Dependencies:**

- All tasks independent (parallel or skip)

**Deliverables:**

- Agent Chat UI documentation
- Node caching (if benchmarks show benefit)
- Time-travel CLI commands

**Success Criteria:**

- Documentation enables Agent Chat UI usage
- Time-travel commands work with existing checkpointer

---

### Critical Path

```text
Week 1 (Phase 1):
Day 1-2: Observability (M1.1) [CRITICAL - blocks all else]
Day 2-4: Testing (M1.2) [HIGH - quality foundation]
Day 4-5: Error Handling (M1.3) [HIGH - resilience]

Week 2 (Phase 2):
Day 6-8: Context & Flexibility (M2.1)
Day 8-9: Resilience & UX (M2.2)
Day 9-10: Deployment (M2.3)

Week 2 (Phase 3 - Optional):
Day 10-11: Power Features (M3.1) [if time permits]
```

**Total Timeline:** 2 weeks
**Minimum Viable:** Phase 1 only (1 week)
**Full Implementation:** Phases 1-3 (2 weeks)

---

## Out of Scope

The following features are explicitly **out of scope** for this enhancement effort:

### Not Included in This PRD

1. **Multi-Tenant Architecture**
   - Rationale: Single-user/single-firewall focus sufficient for MVP
   - Future: Could add in v2.0 if enterprise adoption requires

2. **Custom Web UI Development**
   - Rationale: CLI + Agent Chat UI + deployed API sufficient
   - Alternative: Use existing Agent Chat UI (no development needed)

3. **Batch Multi-Host Operations**
   - Rationale: Single firewall per session keeps scope manageable
   - Alternative: Run multiple sessions in parallel externally

4. **Advanced Caching Strategies**
   - Rationale: Most operations are writes (not cacheable)
   - Approach: Only implement basic caching if benchmarks show >20% benefit

5. **Performance Optimization Beyond Basic Caching**
   - Rationale: Current performance acceptable (<5s for simple queries)
   - Approach: Optimize only if performance issues arise

6. **Alternative LLM Providers (OpenAI, etc.)**
   - Rationale: Anthropic Claude optimized for this use case
   - Future: Could add in v2.0 if demand exists

7. **Mobile Applications**
   - Rationale: CLI + web UI sufficient
   - Future: Not planned

8. **Graphical Workflow Builder**
   - Rationale: YAML workflows simple and flexible
   - Alternative: Document workflow schema thoroughly

9. **Real-Time Collaboration (Multi-User)**
   - Rationale: Single-user sessions sufficient
   - Future: Not planned

10. **Advanced Analytics Dashboard**
    - Rationale: LangSmith provides built-in analytics
    - Alternative: Use LangSmith UI for metrics

---

## Appendix

### A. Glossary

| Term | Definition |
|------|------------|
| **Anonymizer** | Component that masks sensitive data in traces before sending to LangSmith |
| **Checkpointer** | LangGraph component that saves conversation state for resumability |
| **HITL** | Human-in-the-loop, requiring human approval before proceeding |
| **LangSmith** | Observability platform for LLM applications (tracing, debugging, evaluation) |
| **ReAct** | Reasoning + Acting pattern, agent loop: think → act → observe → repeat |
| **Store API** | LangGraph long-term memory API for cross-session persistence |
| **Runtime Context** | Configuration passed to nodes at invocation time (separate from state) |
| **RetryPolicy** | LangGraph mechanism for automatic retries on transient failures |
| **Recursion Limit** | Maximum number of graph steps before GraphRecursionError |
| **Superstep** | Single execution phase in Pregel runtime (all nodes run in parallel) |

---

### B. File References

#### New Files to Create

| File | Purpose | Size | Task |
|------|---------|------|------|
| `src/core/anonymizers.py` | LangSmith anonymization | ~100 lines | 1.2 |
| `src/core/memory_store.py` | Store API helpers | ~150 lines | 4 |
| `src/core/retry_policies.py` | Retry policy definitions | ~50 lines | 3.2 |
| `tests/unit/test_anonymizers.py` | Anonymizer tests | ~200 lines | 1.2 |
| `tests/unit/test_autonomous_nodes.py` | Node unit tests | ~300 lines | 2.1 |
| `tests/unit/test_deterministic_nodes.py` | Node unit tests | ~200 lines | 2.1 |
| `tests/unit/test_tools.py` | Tool unit tests | ~400 lines | 2.1 |
| `tests/unit/test_subgraphs.py` | Subgraph unit tests | ~300 lines | 2.1 |
| `tests/unit/test_memory_store.py` | Store API tests | ~150 lines | 4 |
| `tests/integration/test_autonomous_graph.py` | E2E tests | ~300 lines | 2.2 |
| `tests/integration/test_deterministic_graph.py` | E2E tests | ~250 lines | 2.2 |
| `tests/integration/conftest.py` | Test fixtures | ~100 lines | 2.2 |
| `scripts/evaluate.py` | LangSmith evaluation | ~200 lines | 2.3 |
| `docs/MEMORY_SCHEMA.md` | Memory design docs | ~50 lines | 4 |
| `docs/TROUBLESHOOTING.md` | Troubleshooting guide | ~100 lines | 3.3 |
| `docs/DEPLOYMENT.md` | Deployment guide | ~200 lines | 7 |
| `examples/api_usage.py` | API examples | ~150 lines | 7 |
| `examples/time_travel_examples.py` | Time-travel examples | ~100 lines | 11 |

#### Files to Modify

| File | Changes | Lines | Task |
|------|---------|-------|------|
| `.env.example` | Add LangSmith vars | +3 | 1.1 |
| `src/core/config.py` | LangSmith settings, runtime context | +50 | 1.1, 5 |
| `src/cli/commands.py` | Metadata, timeout, streaming, flags | +100 | 1.3, 3.1, 5, 8, 11 |
| `src/autonomous_graph.py` | Runtime context, Store API, retry | +80 | 4, 5, 3.2 |
| `src/deterministic_graph.py` | Store API, retry | +50 | 4, 3.2 |
| `src/core/subgraphs/deterministic.py` | Recursion handling | +30 | 6 |
| `src/core/subgraphs/crud.py` | Retry policy | +10 | 3.2 |
| `README.md` | Multiple sections | +200 | Various |

---

### C. LangGraph Documentation References

| Topic | Documentation URL | Relevant Tasks |
|-------|-------------------|----------------|
| Anonymizers | <https://docs.smith.langchain.com/how_to_guides/anonymization> | 1.2 |
| Testing | <https://langchain-ai.github.io/langgraph/how-tos/testing/> | 2.1, 2.2 |
| Store API | <https://langchain-ai.github.io/langgraph/how-tos/memory/> | 4 |
| Runtime Context | <https://langchain-ai.github.io/langgraph/use-graph-api#add-runtime-configuration> | 5 |
| RetryPolicy | <https://langchain-ai.github.io/langgraph/how-tos/resilience/> | 3.2 |
| Streaming | <https://langchain-ai.github.io/langgraph/how-tos/stream-updates/> | 8 |
| Deployment | <https://langchain-ai.github.io/langgraph/cloud/deployment/> | 7 |
| Agent Chat UI | <https://github.com/langchain-ai/agent-chat-ui> | 9 |

---

### D. Recommendation Files

All 25 recommendation files in `docs/recommendations/` (00-24):

| File | Status | Priority |
|------|--------|----------|
| 00-overview.md | ✅ Aligned | N/A |
| 01-release-notes.md | ✅ Aligned | N/A |
| 02-migration.md | ✅ Aligned | N/A |
| 03-install.md | ✅ Aligned | N/A |
| 04-quickstart.md | ✅ Aligned | N/A |
| 05-local.md | ✅ Aligned | N/A |
| 06-thinking.md | ✅ Aligned | N/A |
| 07-persistence.md | ✅ Aligned | N/A |
| 08-durable-execution.md | ⚠️ Recommendations | MEDIUM-HIGH |
| 09-streaming.md | ⚠️ Recommendations | MEDIUM-HIGH |
| 10-interrupts.md | ✅ Aligned | N/A |
| 11-time-travel.md | 🔶 Feature Not Exposed | LOW |
| 12-add-memory.md | ❌ Not Implemented | MEDIUM |
| 13-subgraphs.md | ✅ Aligned | N/A |
| 14-app-structure.md | ✅ Aligned | N/A |
| 15-studio.md | ✅ Ready | N/A |
| 16-test.md | ❌ Not Implemented | HIGH |
| 17-deploy.md | ✅ Ready | MEDIUM |
| 18-agent-chat-ui.md | 🔶 Not Integrated | LOW |
| 19-observability.md | ❌ Not Implemented | CRITICAL |
| 20-graph-api.md | ⚠️ Optional Enhancements | MEDIUM |
| 21-use-the-graph-api.md | ⚠️ Optional Enhancements | MEDIUM |
| 22-functional-api.md | ℹ️ Not Applicable | N/A |
| 23-use-functional-api.md | ℹ️ Not Applicable | N/A |
| 24-runtime.md | ℹ️ Informational | N/A |

---

### E. Acceptance Checklist

Use this checklist to verify PRD implementation:

#### Phase 1: Production Readiness (Acceptance Criteria)

- [ ] Anonymizers mask all 4 sensitive data patterns (LUFRPT, sk-ant-, password, XML)
- [ ] LangSmith tracing enabled with anonymization
- [ ] Manual review of 10 traces shows zero leakage
- [ ] Unit tests achieve >80% coverage on critical paths
- [ ] Integration tests cover both graph modes
- [ ] All tests pass in CI
- [ ] Timeout handling prevents hung operations
- [ ] Retry policies reduce transient failures to <1%
- [ ] Documentation explains resume strategies

#### Phase 2: Robustness

- [ ] Store API remembers firewall configs and workflow history
- [ ] Agent uses memory context in prompts
- [ ] Runtime context enables model selection via CLI
- [ ] Recursion handling supports 50+ step workflows
- [ ] Deployment docs enable setup in <5 steps
- [ ] API examples work with deployed agent
- [ ] Streaming provides real-time feedback

#### Phase 3: Optional

- [ ] Agent Chat UI documented and tested
- [ ] Caching implemented if benchmarks show >20% benefit
- [ ] Time-travel CLI commands work (history, show-checkpoint, fork)

---

### F. Stakeholder Sign-Off

| Role | Name | Approval | Date |
|------|------|----------|------|
| Product Owner | [Name] | ☐ Approved | YYYY-MM-DD |
| Technical Lead | [Name] | ☐ Approved | YYYY-MM-DD |
| Security Lead | [Name] | ☐ Approved | YYYY-MM-DD |
| Operations Lead | [Name] | ☐ Approved | YYYY-MM-DD |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-08 | Development Team | Initial PRD based on LangGraph v1.0.0 review |

---

### End of Document
