# Prisma AIRS Python Tools

4 Python projects for integrating with the Palo Alto Networks AI Runtime Security (AIRS) API for prompt scanning, batch analysis, and stress testing.

## What Is Prisma AIRS?

Prisma AIRS provides AI security capabilities including prompt injection detection, data leakage prevention, and content safety scanning for LLM-powered applications. These tools automate interactions with the AIRS API.

## Projects

| Project | Description |
|---------|-------------|
| [batch-scanner](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/prisma-airs/batch-scanner) | CLI tool for bulk-scanning prompt/response pairs from CSV/JSON/YAML files concurrently with `asyncio`. Displays tabular results categorizing entries as malicious or benign with per-violation-type counts. |
| [mcp-server](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/prisma-airs/mcp-server) | FastMCP-based Model Context Protocol server exposing AIRS scanning as MCP tools (`pan_inline_scan`, `pan_batch_scan`, `pan_get_scan_results`, `pan_get_scan_reports`). Includes Kubernetes manifests for production deployment. |
| [scan-csv](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/prisma-airs/scan-csv) | Reads prompts from a CSV file and scans each synchronously through the AIRS API with retry logic, writing action, category, scan ID, round-trip time, and HTTP status to an output CSV. |
| [stress-test](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/python/prisma-airs/stress-test) | Click-based CLI (`prisma-stress`) that drives concurrent HTTP/2 sessions against the AIRS async scan API, collecting metrics and generating markdown reports with percentile response times. |

## Common Setup

All Prisma AIRS projects require an AIRS API key:

```bash
cp .env.example .env
# Set PANW_AI_SEC_API_KEY and PANW_AI_PROFILE_ID or PANW_AI_PROFILE_NAME
```
