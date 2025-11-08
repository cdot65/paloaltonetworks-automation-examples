# LangSmith Evaluation Dataset

## Overview

This document defines the evaluation dataset for the PAN-OS Agent, used to measure performance, accuracy, and reliability across different operation types.

## Dataset: panos-agent-eval-v1

### Categories

1. **Simple List Operations** - Basic read-only queries
2. **CRUD Create** - Object creation operations
3. **CRUD Read** - Object retrieval operations
4. **CRUD Update** - Object modification operations
5. **CRUD Delete** - Object deletion operations
6. **Multi-step Operations** - Complex queries requiring multiple tools
7. **Error Handling** - Invalid inputs and edge cases
8. **Workflows** - Deterministic workflow execution

### Success Metrics

**Primary Metrics:**
- **Success Rate** - % of examples completed successfully
- **Tool Accuracy** - % of examples using correct tool(s)
- **Response Completeness** - % of examples with complete answers
- **Error Handling** - % of error cases handled gracefully

**Secondary Metrics:**
- **Token Efficiency** - Average tokens per operation
- **Execution Time** - Average time per operation
- **Retry Count** - Number of retries needed

**Thresholds:**
- Success Rate: ≥90% (target)
- Tool Accuracy: ≥95% (target)
- Error Handling: 100% (must gracefully handle all errors)
- Token Efficiency: <10k tokens/operation average

---

## Example Definitions

### 1. Simple List Operations (4 examples)

**Example 1: List Address Objects**
```json
{
  "input": "List all address objects",
  "expected_tool": "address_list",
  "expected_output_contains": ["address", "objects", "found"],
  "mode": "autonomous",
  "category": "simple_list"
}
```

**Example 2: List Service Objects**
```json
{
  "input": "List all service objects",
  "expected_tool": "service_list",
  "expected_output_contains": ["service", "objects"],
  "mode": "autonomous",
  "category": "simple_list"
}
```

**Example 3: Show Security Policies**
```json
{
  "input": "Show all security policies",
  "expected_tool": "security_policy_list",
  "expected_output_contains": ["security", "policies"],
  "mode": "autonomous",
  "category": "simple_list"
}
```

**Example 4: List NAT Policies**
```json
{
  "input": "List all NAT policies",
  "expected_tool": "nat_policy_list",
  "expected_output_contains": ["nat", "policies"],
  "mode": "autonomous",
  "category": "simple_list"
}
```

---

### 2. CRUD Create Operations (3 examples)

**Example 5: Create Address Object**
```json
{
  "input": "Create address object web-server at 192.168.1.100",
  "expected_tool": "address_create",
  "expected_output_contains": ["created", "web-server", "192.168.1.100"],
  "mode": "autonomous",
  "category": "crud_create"
}
```

**Example 6: Create Service Object**
```json
{
  "input": "Create service http-8080 using TCP port 8080",
  "expected_tool": "service_create",
  "expected_output_contains": ["created", "service", "8080"],
  "mode": "autonomous",
  "category": "crud_create"
}
```

**Example 7: Create Address Group**
```json
{
  "input": "Create address group web-servers",
  "expected_tool": "address_group_create",
  "expected_output_contains": ["created", "group", "web-servers"],
  "mode": "autonomous",
  "category": "crud_create"
}
```

---

### 3. CRUD Read Operations (2 examples)

**Example 8: Get Address Object**
```json
{
  "input": "Show me the address object named web-server",
  "expected_tool": "address_read",
  "expected_output_contains": ["web-server"],
  "mode": "autonomous",
  "category": "crud_read"
}
```

**Example 9: Get Service Details**
```json
{
  "input": "What are the details of service http-8080?",
  "expected_tool": "service_read",
  "expected_output_contains": ["http-8080", "tcp", "8080"],
  "mode": "autonomous",
  "category": "crud_read"
}
```

---

### 4. CRUD Delete Operations (2 examples)

**Example 10: Delete Address Object**
```json
{
  "input": "Delete address object test-server",
  "expected_tool": "address_delete",
  "expected_output_contains": ["deleted", "test-server"],
  "mode": "autonomous",
  "category": "crud_delete"
}
```

**Example 11: Delete Service Object**
```json
{
  "input": "Remove service test-service",
  "expected_tool": "service_delete",
  "expected_output_contains": ["deleted", "removed", "test-service"],
  "mode": "autonomous",
  "category": "crud_delete"
}
```

---

### 5. Multi-step Operations (2 examples)

**Example 12: Multiple Creates**
```json
{
  "input": "Create address server1 at 10.1.1.1, then create address server2 at 10.1.1.2",
  "expected_tools": ["address_create", "address_create"],
  "expected_output_contains": ["server1", "server2", "10.1.1.1", "10.1.1.2"],
  "mode": "autonomous",
  "category": "multi_step"
}
```

**Example 13: Create and Verify**
```json
{
  "input": "Create address db-server at 10.2.2.10 and then show me its details",
  "expected_tools": ["address_create", "address_read"],
  "expected_output_contains": ["db-server", "10.2.2.10"],
  "mode": "autonomous",
  "category": "multi_step"
}
```

---

### 6. Error Handling (3 examples)

**Example 14: Invalid IP Address**
```json
{
  "input": "Create address bad-server at 999.999.999.999",
  "expected_behavior": "error_handling",
  "expected_output_contains": ["error", "invalid", "ip"],
  "mode": "autonomous",
  "category": "error_case"
}
```

**Example 15: Object Not Found**
```json
{
  "input": "Show me address object nonexistent-server",
  "expected_behavior": "error_handling",
  "expected_output_contains": ["not found", "does not exist"],
  "mode": "autonomous",
  "category": "error_case"
}
```

**Example 16: Duplicate Object**
```json
{
  "input": "Create address existing-server at 10.3.3.3 (when it already exists)",
  "expected_behavior": "error_handling",
  "expected_output_contains": ["already exists", "duplicate"],
  "mode": "autonomous",
  "category": "error_case"
}
```

---

### 7. Deterministic Workflows (3 examples)

**Example 17: Simple Address Workflow**
```json
{
  "input": "workflow: simple_address",
  "expected_steps": 2,
  "expected_output_contains": ["workflow", "complete", "2/2"],
  "mode": "deterministic",
  "category": "workflow"
}
```

**Example 18: Web Server Setup Workflow**
```json
{
  "input": "workflow: web_server_setup",
  "expected_steps": 4,
  "expected_output_contains": ["workflow", "complete"],
  "mode": "deterministic",
  "category": "workflow"
}
```

**Example 19: Security Rule Workflow**
```json
{
  "input": "workflow: security_rule_complete",
  "expected_steps": 3,
  "expected_output_contains": ["workflow", "security", "rule"],
  "mode": "deterministic",
  "category": "workflow"
}
```

---

## Creating the Dataset in LangSmith

### Step 1: Login to LangSmith
```bash
# Visit https://smith.langchain.com
# Create account or login
```

### Step 2: Create Dataset
1. Navigate to **Datasets** tab
2. Click **New Dataset**
3. Name: `panos-agent-eval-v1`
4. Description: "Evaluation dataset for PAN-OS Agent v0.1.0"

### Step 3: Add Examples
For each example above:
1. Click **Add Example**
2. Fill in:
   - **Input**: The user query/command
   - **Expected Output**: (optional) Expected response patterns
   - **Metadata**: Add category, mode, expected_tool, etc.
3. Click **Save**

### Step 4: Tag and Organize
- Add tags: `panos-agent`, `v0.1.0`, category names
- Use metadata to filter during evaluation

---

## Running Evaluation

### Using Example Dataset (Current)
```bash
# Evaluate both modes
python scripts/evaluate.py --mode both --save-results

# Evaluate autonomous only
python scripts/evaluate.py --mode autonomous

# Evaluate deterministic only
python scripts/evaluate.py --mode deterministic
```

### Using LangSmith Dataset (Future)
```bash
# After dataset created in LangSmith
python scripts/evaluate.py --dataset panos-agent-eval-v1 --mode both
```

---

## Interpreting Results

### Success Rate Thresholds

**Excellent (≥95%)**
- Production-ready
- High confidence in accuracy

**Good (90-94%)**
- Acceptable for production
- Monitor for regressions

**Needs Improvement (80-89%)**
- Address failing cases
- Review tool selection logic

**Critical (<80%)**
- Do not deploy
- Major refactoring needed

### Token Efficiency

**Efficient (<8k tokens/operation)**
- Cost-effective
- Fast responses

**Acceptable (8k-12k tokens/operation)**
- Monitor costs
- Consider optimization

**Inefficient (>12k tokens/operation)**
- Investigate long conversations
- Optimize prompts
- Consider model downgrade

---

## Continuous Evaluation

### Weekly Regression Testing
```bash
# Run evaluation weekly
python scripts/evaluate.py --mode both --save-results

# Compare to baseline
# Alert if success rate drops >5%
```

### Pre-Deployment Validation
```bash
# Before deploying new version
python scripts/evaluate.py --mode both --save-results

# Ensure success rate ≥90%
# Ensure no critical regressions
```

### A/B Testing
```bash
# Test new model/prompt version
# Compare metrics to current version
# Deploy if improvement >2%
```

---

## Future Enhancements

1. **LangSmith Integration**
   - Upload examples to LangSmith
   - Use LangSmith evaluation API
   - Automatic alerts on regressions

2. **Expanded Dataset**
   - Add 10+ examples per category
   - Cover edge cases
   - Include performance benchmarks

3. **Custom Evaluators**
   - Tool selection accuracy evaluator
   - Response completeness evaluator
   - Error handling evaluator

4. **Automated Alerts**
   - Slack/email on regression
   - Weekly summary reports
   - Cost monitoring alerts

---

**Last Updated:** 2025-01-08
**Dataset Version:** v1 (example dataset)
**Production Status:** Development (LangSmith upload pending)
