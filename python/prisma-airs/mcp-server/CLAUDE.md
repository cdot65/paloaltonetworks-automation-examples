# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server implementation for Palo Alto Networks AI Security. The MCP server provides a standardized interface for AI assistants to interact with Palo Alto Networks AI Security features, enabling security scanning and threat detection capabilities within AI workflows.

## Development Setup

### Initial Setup
```bash
# Create virtual environment with uv
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies including dev dependencies
uv pip install -e ".[dev]"

# Set up environment variables
cp .env.example .env
# Edit .env with your PANW_AI_SEC_API_KEY and profile configuration
```

### Key Dependencies
- **pan-aisecurity** (0.4.1a2): Palo Alto Networks AI Security SDK
- **python-dotenv**: Environment variable management
- Python 3.12+ required

## Project Architecture

### MCP Server Structure
When implementing the MCP server, follow these patterns:

1. **Server Entry Point**: Create `src/server.py` as the main MCP server implementation
2. **Protocol Handlers**: Implement MCP protocol handlers for:
   - Tool registration (exposing AI Security capabilities)
   - Request handling (processing security scan requests)
   - Response formatting (returning scan results in MCP format)

3. **AI Security Integration**: Use the `pan-aisecurity` SDK to:
   - Submit prompts/responses for security scanning
   - Retrieve scan results
   - Handle batch operations if needed

## MCP Implementation Guidelines

1. **Tool Registration**: Register tools that expose AI Security capabilities:
   - `scan_prompt`: Submit a prompt for security scanning
   - `scan_conversation`: Submit prompt/response pairs
   - `get_scan_results`: Retrieve results by batch ID
   - `list_profiles`: List available AI security profiles

2. **Error Handling**: Implement proper error handling for:
   - API authentication failures
   - Network timeouts
   - Invalid profile configurations
   - Rate limiting

3. **Configuration**: Support configuration via:
   - Environment variables (primary method)
   - MCP server configuration
   - Runtime parameters

## Related Examples

The `airuntime-security-batch` project in the same repository provides a good reference for:
- Interacting with the pan-aisecurity SDK
- Handling batch operations
- Processing scan results
- Error handling patterns

## Environment Variables

Required environment variables (create `.env` from `.env.example`):
- `PANW_AI_SEC_API_KEY`: API key for AI Security service
- `PANW_AI_PROFILE_ID` or `PANW_AI_PROFILE_NAME`: AI security profile configuration
- `PANW_AI_SEC_API_ENDPOINT` (optional): Custom API endpoint
