# Troubleshooting Guide

Comprehensive guide for diagnosing and resolving common issues with the PAN-OS Agent.

## Table of Contents

- [Connection Issues](#connection-issues)
- [Timeout Errors](#timeout-errors)
- [Tool Execution Failures](#tool-execution-failures)
- [Checkpoint and Resume Issues](#checkpoint-and-resume-issues)
- [Workflow Errors](#workflow-errors)
- [Performance Issues](#performance-issues)
- [LangSmith Tracing](#langsmith-tracing)

---

## Connection Issues

### Firewall Connection Timeout

**Symptom:**
```
❌ Error: PanConnectionTimeout: Connection to 192.168.1.1 timed out
```

**Cause:**
- Firewall unreachable (network routing, firewall down)
- Firewall overloaded or hung
- Incorrect hostname/IP in configuration

**Resolution:**

1. **Verify connectivity:**
   ```bash
   ping 192.168.1.1
   telnet 192.168.1.1 443
   ```

2. **Check credentials:**
   ```bash
   panos-agent test-connection
   ```

3. **Verify environment variables:**
   ```bash
   cat .env | grep PANOS
   # Should show: PANOS_HOSTNAME, PANOS_USERNAME, PANOS_PASSWORD
   ```

4. **Check firewall health** via GUI or another method

5. **Resume after fixing:**
   ```bash
   # Use same thread ID to resume
   panos-agent run -p "Continue from where we left off" --thread-id <same-id>
   ```

**Automatic Retry:**
Connection timeouts are automatically retried 3 times with exponential backoff (2s, 4s, 8s). If all retries fail, manual intervention is needed.

---

### Invalid API Credentials

**Symptom:**
```
❌ Error: PanDeviceError: Authentication failed
```

**Cause:**
- Wrong username or password
- Account locked or disabled
- Insufficient permissions

**Resolution:**

1. **Verify credentials in `.env`:**
   ```bash
   PANOS_USERNAME=admin
   PANOS_PASSWORD=your_actual_password
   ```

2. **Test manually via curl:**
   ```bash
   curl -k -u admin:password https://192.168.1.1/api/?type=keygen
   ```

3. **Check account status** in firewall GUI
4. **Verify user has API access permissions**

**Not Automatically Retried:**
Authentication errors are permanent and fail immediately. Fix credentials and retry with a new thread ID.

---

## Timeout Errors

### Graph Execution Timeout

**Symptom:**
```
Timeout Error: Graph execution exceeded 300.0s timeout
Mode: autonomous
Thread ID: abc-123-def
Prompt preview: Create 100 address objects...
```

**Cause:**
- Operation taking longer than timeout allows
- Agent stuck in reasoning loop
- Large batch operation

**Resolution:**

1. **Resume with same thread ID:**
   ```bash
   # Agent will continue from last checkpoint
   panos-agent run -p "Continue the operation" --thread-id abc-123-def
   ```

2. **Increase timeout (if needed):**
   Edit `src/core/config.py`:
   ```python
   TIMEOUT_AUTONOMOUS = 600.0  # Increase to 10 minutes
   TIMEOUT_DETERMINISTIC = 1200.0  # Increase to 20 minutes
   ```

3. **Break into smaller operations:**
   ```bash
   # Instead of "Create 100 objects"
   panos-agent run -p "Create 25 address objects batch 1" -m autonomous
   panos-agent run -p "Create 25 address objects batch 2" -m autonomous
   # etc.
   ```

**When to Increase Timeouts:**
- Complex workflows with 10+ steps
- Large batch operations (50+ objects)
- Slow firewall hardware or large configs

---

### Commit Timeout

**Symptom:**
```
❌ Error: Commit operation timed out after 180s
```

**Cause:**
- Large configuration changes requiring long commit
- Firewall under heavy load
- Commit already in progress

**Resolution:**

1. **Check commit status** via firewall GUI
2. **Wait for current commit to finish**, then retry
3. **Increase commit timeout:**
   Edit `src/core/config.py`:
   ```python
   TIMEOUT_COMMIT = 300.0  # Increase to 5 minutes
   ```

4. **Resume workflow:**
   ```bash
   panos-agent run -p "Retry the commit" --thread-id <same-id>
   ```

**Automatic Retry:**
Commit operations retry once (2 attempts total) with 1.5s backoff. If both fail, check firewall manually.

---

## Tool Execution Failures

### Object Already Exists

**Symptom:**
```
❌ Error: PanDeviceError: Object 'web-server' already exists
```

**Cause:**
- Attempting to create duplicate object
- Previous operation succeeded but appeared to fail
- Resuming from checkpoint without awareness

**Resolution:**

1. **Continue with context in same thread:**
   ```bash
   # Agent will understand the object exists
   panos-agent run -p "The object already exists, skip it and continue" --thread-id <same-id>
   ```

2. **Or use update instead of create:**
   ```bash
   panos-agent run -p "Update the existing web-server object instead" --thread-id <same-id>
   ```

3. **Or start fresh with new thread:**
   ```bash
   panos-agent run -p "List address objects" -m autonomous
   # New conversation, no history
   ```

**Not Automatically Retried:**
Duplicate object errors are permanent. Use update or skip the object.

---

### Object Not Found

**Symptom:**
```
❌ Error: PanDeviceError: Object 'missing-server' does not exist
```

**Cause:**
- Typo in object name
- Object was deleted
- Wrong search location (vsys, device group)

**Resolution:**

1. **List objects to verify:**
   ```bash
   panos-agent run -p "List all address objects" -m autonomous
   ```

2. **Correct the name:**
   ```bash
   panos-agent run -p "I meant 'web-server' not 'missing-server'" --thread-id <same-id>
   ```

3. **Create it first:**
   ```bash
   panos-agent run -p "First create the object, then continue" --thread-id <same-id>
   ```

---

### Invalid Configuration

**Symptom:**
```
❌ Error: PanDeviceError: Invalid IP address format: '256.1.1.1'
```

**Cause:**
- Invalid input parameters (IP, port, etc.)
- Malformed XML/JSON
- Missing required fields

**Resolution:**

1. **Correct input and retry:**
   ```bash
   panos-agent run -p "Use 192.168.1.1 instead of 256.1.1.1" --thread-id <same-id>
   ```

2. **Verify format requirements** in PAN-OS documentation

**Not Automatically Retried:**
Validation errors are permanent. Fix input and retry with same thread ID.

---

## Checkpoint and Resume Issues

### Lost Checkpoint Data

**Symptom:**
Agent doesn't remember previous conversation when using same thread ID.

**Cause:**
- Checkpointer using in-memory storage (resets on restart)
- Typo in thread ID
- Using different mode (autonomous vs deterministic)

**Resolution:**

1. **Verify thread ID:**
   ```bash
   # Check output from previous run
   Thread ID: abc-123-def

   # Use exact same ID
   panos-agent run -p "Continue" --thread-id abc-123-def
   ```

2. **Use persistent checkpointer (future enhancement):**
   Currently using `MemorySaver` (in-memory). For persistence across restarts, upgrade to SQLite checkpointer.

3. **LangGraph Studio shows checkpoint history:**
   ```bash
   langgraph dev
   # Open http://localhost:8000
   # View checkpoint history for thread
   ```

---

### Cannot Resume Workflow

**Symptom:**
Workflow doesn't resume from failure point.

**Cause:**
- Using different thread ID
- Starting new workflow instead of resuming
- Checkpoint corruption

**Resolution:**

1. **Use same thread ID and mode:**
   ```bash
   # Original failed run
   panos-agent run -p "complex_workflow" -m deterministic --thread-id wf-001

   # Resume (same thread ID, same mode)
   panos-agent run -p "complex_workflow" -m deterministic --thread-id wf-001
   ```

2. **Check checkpoint state in LangGraph Studio**

3. **If corrupted, start fresh:**
   ```bash
   panos-agent run -p "complex_workflow" -m deterministic --thread-id wf-002
   ```

---

### Time-Travel / Forking from Checkpoint

**Feature:** View and fork from historical checkpoints (planned CLI commands)

**Current Workaround:**

1. **Use LangGraph Studio:**
   ```bash
   langgraph dev
   ```

2. **Navigate to thread** → View checkpoint history

3. **Manually fork:**
   - Select historical checkpoint
   - Create new thread with that state
   - Continue from that point

**Future CLI Commands (Planned):**
```bash
# View checkpoint history
panos-agent history --thread-id abc-123

# Show specific checkpoint
panos-agent show-checkpoint --thread-id abc-123 --checkpoint-id xyz

# Fork from checkpoint
panos-agent fork --from-thread abc-123 --from-checkpoint xyz --to-thread new-456
```

---

## Workflow Errors

### Workflow Not Found

**Symptom:**
```
❌ Error: No steps defined for workflow 'missing_workflow'
```

**Cause:**
- Typo in workflow name
- Workflow not defined in `src/workflows/definitions.py`

**Resolution:**

1. **List available workflows:**
   ```bash
   panos-agent list-workflows
   ```

2. **Use correct name:**
   ```bash
   panos-agent run -p "simple_address" -m deterministic
   ```

3. **Create custom workflow** (see `docs/ARCHITECTURE.md`)

---

### Workflow Step Failure

**Symptom:**
```
📊 Workflow 'web_server_setup' Execution Summary
Steps: 3/5
✅ Successful: 2
❌ Failed: 1

  1. ✅ Create address object
  2. ✅ Create service object
  3. ❌ Create security rule
     Error: Referenced object 'missing-zone' does not exist
```

**Cause:**
- Tool execution failed at specific step
- Missing dependencies
- Invalid parameters in workflow definition

**Resolution:**

1. **Fix dependency and resume:**
   ```bash
   # Create missing dependency
   panos-agent run -p "Create zone 'missing-zone'" -m autonomous

   # Resume workflow with same thread
   panos-agent run -p "web_server_setup" -m deterministic --thread-id <same-id>
   ```

2. **Skip failed step manually:**
   ```bash
   panos-agent run -p "Skip the security rule and continue" --thread-id <same-id>
   ```

3. **Edit workflow definition** if parameters are wrong

---

## Performance Issues

### Slow Response Times

**Symptom:**
Agent takes 30+ seconds to respond.

**Cause:**
- Large firewall configuration (1000+ objects)
- Slow LLM API response
- Network latency to firewall

**Resolution:**

1. **Use faster model:**
   Currently using `claude-haiku-4-5`. This is already the fastest model.

2. **Reduce log level:**
   ```bash
   panos-agent run -p "..." --log-level ERROR
   ```

3. **Check network latency:**
   ```bash
   time panos-agent test-connection
   ```

4. **Optimize workflow** - reduce number of list operations

---

### High Token Usage

**Symptom:**
LangSmith shows high token counts per operation.

**Cause:**
- Large conversation history
- Many tool calls
- Verbose responses

**Resolution:**

1. **Start fresh thread** for new tasks:
   ```bash
   # Don't reuse thread for unrelated tasks
   panos-agent run -p "New task" -m autonomous  # Auto-generates thread ID
   ```

2. **Use deterministic mode** for predictable operations:
   ```bash
   # Deterministic uses fewer tokens (no ReAct loop)
   panos-agent run -p "simple_address" -m deterministic
   ```

3. **Monitor in LangSmith:**
   - Filter by tag: `panos-agent`
   - Check metadata: `user_prompt_length`, token counts

---

## LangSmith Tracing

### Traces Not Appearing in LangSmith

**Symptom:**
No traces visible in LangSmith dashboard.

**Cause:**
- Tracing not enabled
- Wrong API key
- Wrong project name

**Resolution:**

1. **Verify environment variables:**
   ```bash
   cat .env | grep LANGSMITH
   LANGSMITH_TRACING=true
   LANGSMITH_API_KEY=lsv2_pt_...
   LANGSMITH_PROJECT=panos-agent-prod
   ```

2. **Test API key:**
   ```bash
   curl -H "x-api-key: ${LANGSMITH_API_KEY}" https://api.smith.langchain.com/info
   ```

3. **Run operation and check:**
   ```bash
   panos-agent run -p "Test trace" -m autonomous
   # Check LangSmith UI for new trace
   ```

---

### Sensitive Data in Traces

**Symptom:**
Worried about credentials appearing in LangSmith traces.

**Cause:**
User concern (valid!).

**Resolution:**

**Good news:** All traces are automatically anonymized before sending to LangSmith.

**Anonymized data:**
- PAN-OS API keys → `<panos-api-key>`
- Anthropic API keys → `<anthropic-api-key>`
- Password fields → `password: <password>`
- XML passwords → `<password><redacted></password>`

**Verify anonymization:**
1. Run operation with sensitive data
2. Check trace in LangSmith
3. Confirm passwords/keys are masked

**Testing:**
See `tests/unit/test_anonymizers.py` for anonymization test coverage.

---

## Getting Help

### Debugging Checklist

Before filing an issue, try:

1. ✅ Test firewall connectivity: `panos-agent test-connection`
2. ✅ Check environment variables: `cat .env`
3. ✅ Review logs with `--log-level DEBUG`
4. ✅ Try resuming with same thread ID
5. ✅ Check LangSmith traces (if enabled)
6. ✅ Review checkpoint history in LangGraph Studio

### Filing an Issue

Include:

1. **Command run:**
   ```bash
   panos-agent run -p "..." -m autonomous --thread-id abc-123
   ```

2. **Error message:**
   ```
   Full error output here
   ```

3. **Environment:**
   - PAN-OS version: 11.1.4
   - Python version: 3.11
   - Agent version: 0.1.0

4. **LangSmith trace URL** (if available and sanitized)

5. **Reproduction steps**

### Useful Commands

```bash
# Test connection
panos-agent test-connection

# View version
panos-agent version

# List workflows
panos-agent list-workflows

# Run with debug logging
panos-agent run -p "..." --log-level DEBUG

# Start LangGraph Studio
langgraph dev
```

---

## Related Documentation

- **[README.md](../README.md)** - Main documentation and quickstart
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture and design
- **[SETUP.md](SETUP.md)** - Development environment setup

---

**Last Updated:** 2025-01-08
**Version:** 0.1.0
