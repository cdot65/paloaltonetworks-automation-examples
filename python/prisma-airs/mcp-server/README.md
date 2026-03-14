# Prisma AIRS MCP Server

## Overview

A Model Context Protocol (MCP) server that exposes Palo Alto Networks AI Runtime Security (AIRS) scanning capabilities as MCP tools. Built with FastMCP and the `pan-aisecurity` SDK, it enables AI assistants and LLM workflows to perform synchronous inline scans, asynchronous batch scans, and retrieve scan results and threat reports via the standard MCP interface. The server supports SSE transport and includes Kubernetes manifests for production deployment with Traefik ingress, horizontal pod autoscaling, and session affinity.

## Prerequisites

- Python 3.10+
- `uv` package manager
- A Palo Alto Networks AI Runtime Security API key and AI Profile
- Docker (for container builds, optional)
- Kubernetes cluster with Traefik (for production deployment, optional)

## Quickstart

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/prisma-airs/mcp-server
   ```

2. **Create and activate a virtual environment:**

   ```bash
   uv venv
   source .venv/bin/activate
   ```

   > **Tip -- What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python. This prevents version conflicts between projects.

3. **Install dependencies:**

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configure credentials:**

   Create a `.env` file with your AIRS credentials (see Configuration below).

5. **Run the MCP server:**

   ```bash
   uv run fastmcp run -t sse main.py
   ```

## Configuration

Create a `.env` file in the project root:

```
PANW_AI_SEC_API_KEY=your-api-key-here
PANW_AI_PROFILE_NAME=your-profile-name-here
# PANW_AI_PROFILE_ID=your-profile-id-here
# PANW_AI_SEC_API_ENDPOINT=https://service.api.aisecurity.paloaltonetworks.com
```

| Variable | Required | Description |
|---|---|---|
| `PANW_AI_SEC_API_KEY` | Yes | AIRS API key |
| `PANW_AI_PROFILE_NAME` | One of Name or ID | AI Profile human-readable name |
| `PANW_AI_PROFILE_ID` | One of Name or ID | AI Profile UUID |
| `PANW_AI_SEC_API_ENDPOINT` | No | Custom API endpoint (defaults to US region) |

**Security note:** Never commit `.env` files or API keys to version control.

## Usage

**Run locally with SSE transport:**

```bash
uv run fastmcp run -t sse main.py
```

**Run via Docker:**

```bash
docker build -t aisecurity-mcp-server .
docker run -p 8000:8000 --env-file .env aisecurity-mcp-server
```

**Deploy to Kubernetes:**

```bash
kubectl apply -f aisecurity-mcp.yaml
kubectl apply -f traefik-routes.yaml
```

### MCP Tools

The server exposes four tools:

- **`pan_inline_scan`** -- Synchronous scan of a single prompt and/or response. Returns category (benign/malicious) and action (allow/block).
- **`pan_batch_scan`** -- Asynchronous batch scan of multiple prompt/response pairs. Auto-splits into batches of 5 submitted concurrently. Returns scan IDs and report IDs.
- **`pan_get_scan_results`** -- Retrieve scan results by a list of scan ID UUIDs.
- **`pan_get_scan_reports`** -- Retrieve threat scan reports by report IDs (scan ID prefixed with "R").

### Expected Output

When an MCP client calls `pan_inline_scan` with a prompt, the server returns a `ScanResponse` object:

```json
{
  "action": "block",
  "category": "malicious",
  "scan_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "report_id": "Ra1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "profile_name": "Prisma AIRS",
  "prompt_detected": {
    "dlp": true,
    "injection": false,
    "toxic_content": false,
    "url_cats": false
  },
  "response_detected": {
    "dlp": false,
    "toxic_content": false,
    "url_cats": false
  }
}
```

For `pan_batch_scan`, the server returns a list of `AsyncScanResponse` objects each containing `scan_id` and `report_id` for subsequent retrieval.

## Project Structure

```
mcp-server/
  main.py               # MCP server with all tool definitions and SDK integration
  requirements.txt      # Dependencies (pan-aisecurity, fastmcp, python-dotenv)
  Dockerfile            # Multi-stage container build (Python 3.12 slim, non-root user)
  aisecurity-mcp.yaml   # Kubernetes Deployment, Service, HPA, Secrets, ConfigMap
  traefik-routes.yaml   # Traefik IngressRoute and middleware configuration
  .env                  # Environment variable configuration (not committed)
```

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `ToolError: Missing AI Profile Name or ID` | `PANW_AI_PROFILE_NAME` and `PANW_AI_PROFILE_ID` both unset | Set one of them in `.env` or as an environment variable |
| `ToolError: Must provide at least one of prompt and/or response` | Both `prompt` and `response` are None | Pass at least one non-null value to `pan_inline_scan` |
| `ModuleNotFoundError: No module named 'fastmcp'` | Dependencies not installed | Run `uv pip install -r requirements.txt` |
| SSL certificate verify failed | Corporate proxy or outdated CA certs | Set `PANW_AI_SEC_API_ENDPOINT` or update system CA certificates |
| Connection timeout to AIRS API | Network issues or API downtime | Check network connectivity; verify the API endpoint URL |
| Docker container exits immediately | Missing environment variables | Run with `--env-file .env` or set variables in Kubernetes Secrets |
| Kubernetes SSE connections dropping | No session affinity configured | Apply `traefik-routes.yaml` for sticky sessions and proper timeouts |
