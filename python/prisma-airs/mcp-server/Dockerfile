# Multi-stage build for efficient image
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Final stage
FROM python:3.12-slim

# Install uv in final image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Create non-root user
RUN useradd -m -u 1000 mcpuser

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copy application
COPY main.py .
COPY .env.example .

# Change ownership
RUN chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Set environment variables for MCP SSE transport
ENV FASTMCP_TRANSPORT=sse
ENV FASTMCP_PORT=8000
ENV FASTMCP_HOST=0.0.0.0

# Expose port for SSE transport
EXPOSE 8000

# Note: FastMCP doesn't provide a /health endpoint by default
# Health checks should be handled at the Kubernetes level

# Run the MCP server with SSE transport for k8s
CMD ["uv", "run", "fastmcp", "run", "-t", "sse", "--host", "0.0.0.0", "--port", "8000", "main.py"]