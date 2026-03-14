# Prisma AIRS Stress Testing Tool

## Overview

A performance stress testing tool for Palo Alto Networks AI Runtime Security (AIRS) scanning API endpoints. It uses a CLI (`prisma-stress`) built with Click to drive concurrent HTTP/2 sessions against the AIRS async scan API, collecting real-time metrics and generating detailed markdown reports with response time percentiles, throughput analysis, and scaling recommendations. The tool supports configurable test scenarios defined in YAML, retry logic with tenacity, and circuit breaker patterns for resilient operation under high load.

**Note:** The Python source files for this project are compiled (`.pyc` only). The project structure is documented here based on package metadata, but source modifications require access to the original `.py` files.

## Prerequisites

- Python 3.12+
- `uv` package manager

## Quickstart

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/prisma-airs/stress-test
   ```

2. **Create and activate a virtual environment:**

   ```bash
   uv venv
   source .venv/bin/activate
   ```

   > **Tip -- What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python. This prevents version conflicts between projects.

3. **Install dependencies:**

   ```bash
   uv sync
   ```

4. **Configure a test scenario:**

   Create a YAML config file in the `config/` directory (see Configuration below).

5. **Run a stress test:**

   ```bash
   uv run prisma-stress test --config config/default.yaml
   ```

## Configuration

Create a YAML configuration file:

```yaml
api_endpoints:
  - base_url: "https://service.api.aisecurity.paloaltonetworks.com/v1/scan/async/request"
    api_key: "YOUR_API_KEY"
    profile_id: "YOUR_PROFILE_ID"
    timeout_seconds: 30
    max_retries: 3
    verify_ssl: true

test_scenarios:
  - name: "baseline_load_test"
    duration_seconds: 300
    concurrent_sessions: 10
    requests_per_second: 50
    ramp_up_seconds: 30
    payload_template: "examples/payloads/batch_request.json"

performance_thresholds:
  max_response_time_ms: 500
  min_success_rate: 0.95
  max_error_rate: 0.05

report:
  output_format: "markdown"
  include_charts: true
  output_directory: "reports"
```

| Variable | Required | Description |
|---|---|---|
| `PRISMA_API_KEY` | Yes (env var or in YAML) | AIRS API key |
| `PRISMA_PROFILE_ID` | Yes (env var or in YAML) | AI Profile UUID |
| `api_endpoints[].base_url` | Yes | AIRS async scan API endpoint |
| `test_scenarios[].concurrent_sessions` | Yes | Number of concurrent sessions (1-100) |
| `test_scenarios[].duration_seconds` | Yes | Test duration in seconds |
| `performance_thresholds` | No | Pass/fail thresholds for metrics |

**Security note:** Never commit YAML files containing API keys to version control. Use environment variables for sensitive data.

## Usage

**Run a stress test:**

```bash
uv run prisma-stress test --config config/default.yaml
```

**Dry run to validate configuration:**

```bash
uv run prisma-stress test --config config/my-test.yaml --dry-run
```

**Generate a report from existing results:**

```bash
uv run prisma-stress report --input reports/latest_results.json
```

**Enable verbose logging:**

```bash
uv run prisma-stress test --config config/default.yaml --verbose
```

### Expected Output

The tool generates a markdown report with performance metrics:

```
# Prisma AIRS Stress Test Report

**Test Date**: 2024-01-15 14:30:22
**Duration**: 300 seconds
**Total Requests**: 15,000
**Success Rate**: 97.5%

## Performance Summary

| Metric              | Value   |
|---------------------|---------|
| Average Response Time | 245ms |
| 95th Percentile     | 412ms   |
| 99th Percentile     | 523ms   |
| Throughput          | 50 req/s |

## Concurrent Sessions Analysis

| Sessions | Avg Response (ms) | Success Rate | Throughput |
|----------|--------------------|--------------|------------|
| 10       | 125                | 99.8%        | 80 req/s   |
| 25       | 245                | 98.5%        | 102 req/s  |
| 50       | 412                | 96.2%        | 120 req/s  |
| 100      | 823                | 92.1%        | 115 req/s  |
```

## Project Structure

```
stress-test/
  src/
    prisma_stress/
      __init__.py    # Package init
      cli.py         # Click CLI entry point (prisma-stress command)
      client.py      # HTTP/2 client for AIRS API requests
      config.py      # YAML configuration loading and validation
      engine.py      # Stress test execution engine with concurrency control
      metrics.py     # Performance metrics collection and aggregation
      reporter.py    # Markdown report generation
  pyproject.toml     # Project metadata and dependencies
  uv.lock            # Locked dependency versions
```

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| Authentication errors (HTTP 401/403) | Invalid API key or profile ID | Verify credentials in config YAML or environment variables |
| `ModuleNotFoundError: No module named 'prisma_stress'` | Package not installed | Run `uv sync` to install the project |
| Connection timeouts under load | API rate limiting or network saturation | Reduce `concurrent_sessions` or increase `timeout_seconds` |
| SSL certificate verify failed | Corporate proxy or cert issues | Set `verify_ssl: false` in config (not recommended for production) |
| High error rates in results | Exceeding API rate limits | Lower `requests_per_second` and `concurrent_sessions` |
| Empty report generated | Test duration too short | Increase `duration_seconds` to allow sufficient data collection |
| `FileNotFoundError` for payload template | Missing payload file | Create the payload JSON file at the path specified in `payload_template` |
