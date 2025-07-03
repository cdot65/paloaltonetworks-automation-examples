# AI Security MCP Server for Kubernetes

This repository contains a Model Context Protocol (MCP) server implementation for Palo Alto Networks AI Security, designed to run on Kubernetes with Traefik as the ingress controller.

## Overview

The MCP server provides a standardized interface for AI assistants to interact with Palo Alto Networks AI Security features, enabling security scanning and threat detection capabilities within AI workflows.

## Prerequisites

- Kubernetes cluster (v1.20+)
- kubectl configured to access your cluster
- Docker or similar container runtime for building images
- MetalLB or another LoadBalancer provider (for bare-metal clusters)
- Container registry access (e.g., Docker Hub, GitHub Container Registry)

## Building the Docker Image

1. Clone this repository:
```bash
git clone <repository-url>
cd aisecurity-mcp-server
```

2. Build the Docker image:
```bash
docker build -t <your-registry>/aisecurity-mcp-server:latest .
```

3. Push the image to your container registry:
```bash
docker push <your-registry>/aisecurity-mcp-server:latest
```

### Image Details
- Base image: Python 3.12 slim
- Runs as non-root user (UID 1000)
- Exposes port 8000 for SSE (Server-Sent Events) transport
- Uses FastMCP framework with SSE transport for Kubernetes compatibility

## Configuration

### Environment Variables

Before deploying, update the secrets in `aisecurity-mcp.yaml`:

```yaml
stringData:
  PANW_AI_SEC_API_KEY: "your-actual-api-key"
  PANW_AI_PROFILE_NAME: "your-profile-name"
```

Required environment variables:
- `PANW_AI_SEC_API_KEY`: Your Palo Alto Networks AI Security API key
- `PANW_AI_PROFILE_NAME` or `PANW_AI_PROFILE_ID`: AI security profile configuration

### Update Image Reference

In `aisecurity-mcp.yaml`, update the image reference to your registry:

```yaml
image: <your-registry>/aisecurity-mcp-server:latest
```

## Deployment

Deploy the manifests in the following order:

1. **Deploy Traefik ingress controller:**
```bash
kubectl apply -f traefik.yaml
```

2. **Deploy the MCP server application:**
```bash
kubectl apply -f aisecurity-mcp.yaml
```

3. **Configure Traefik routing:**
```bash
kubectl apply -f traefik-routes.yaml
```

### Verify Deployment

Check that all pods are running:
```bash
kubectl get pods -n aisecurity
```

Expected output:
```
NAME                                     READY   STATUS    RESTARTS   AGE
aisecurity-mcp-server-xxxxxxxxx-xxxxx    1/1     Running   0          1m
aisecurity-mcp-server-xxxxxxxxx-xxxxx    1/1     Running   0          1m
aisecurity-mcp-server-xxxxxxxxx-xxxxx    1/1     Running   0          1m
traefik-xxxxxxxxx-xxxxx                  1/1     Running   0          1m
```

Check services:
```bash
kubectl get svc -n aisecurity
```

## Architecture

### Components

1. **MCP Server Deployment**
   - 3 replicas for high availability
   - Horizontal Pod Autoscaler (HPA) configured
   - Resource limits: 512Mi memory, 500m CPU
   - No health checks (SSE endpoint streams continuously)

2. **Traefik Ingress**
   - LoadBalancer service type (requires MetalLB on bare-metal)
   - Routes `/sse/` path to MCP server pods
   - Dashboard available on port 9000
   - Sticky sessions enabled for SSE connections

3. **Routing Configuration**
   - Only `/sse/` paths are routed to the MCP server
   - All other paths return 404
   - Session affinity ensures clients stay connected to the same pod

## Accessing the Service

### From External Hosts

Once deployed, the service is accessible through the Traefik LoadBalancer IP:

1. Get the external IP:
```bash
kubectl get svc traefik -n aisecurity
```

2. Access the SSE endpoint:
```
http://<EXTERNAL-IP>:8080/sse/
```

### Traefik Dashboard

The Traefik dashboard is available at:
```
http://<EXTERNAL-IP>:9000/dashboard/
```

## Interacting with the MCP Server

The MCP server uses Server-Sent Events (SSE) for communication. To interact with it:

### Using curl:
```bash
# Test SSE connection (will stream events)
curl -N -H "Accept: text/event-stream" http://<EXTERNAL-IP>:8080/sse/
```

### From an MCP Client:
```python
# Example using an MCP client library
from mcp import Client

client = Client(
    transport="sse",
    url="http://<EXTERNAL-IP>:8080/sse/"
)

# Use the available tools
result = await client.call_tool(
    "pan_inline_scan",
    {
        "prompt": "Analyze this text for security threats",
        "response": "Model response to scan"
    }
)
```

### Available MCP Tools

The server exposes the following tools:
- `pan_inline_scan`: Synchronous scanning of prompts/responses
- `pan_batch_scan`: Asynchronous batch scanning
- `pan_get_scan_results`: Retrieve scan results by ID
- `pan_get_scan_reports`: Retrieve detailed threat reports

## Troubleshooting

### Pods Not Ready
- The MCP server pods don't have health checks since `/sse/` is a streaming endpoint
- Pods should show as Running and Ready without health checks

### Cannot Access Service
1. Verify LoadBalancer IP is assigned:
   ```bash
   kubectl get svc traefik -n aisecurity
   ```
2. Check Traefik routes are loaded:
   ```bash
   kubectl get ingressroute -n aisecurity
   ```
3. Check Traefik logs:
   ```bash
   kubectl logs -n aisecurity deployment/traefik
   ```

### Connection Timeouts
- SSE endpoints keep connections open indefinitely
- Timeouts when using curl with `-I` or `--head` are expected
- Use regular GET requests without timeout for SSE streams

## Security Considerations

- The server runs as a non-root user (UID 1000)
- Resource limits are enforced
- Secrets are stored in Kubernetes Secrets (consider using sealed-secrets or external secret managers for production)
- No TLS by default (add TLS termination at Traefik for production)

## Scaling

The deployment includes:
- Horizontal Pod Autoscaler (HPA) configured for 2-10 replicas
- Scales based on CPU (70%) and memory (80%) utilization
- Session affinity ensures SSE connections remain stable during scaling

## MetalLB Requirement

This deployment requires MetalLB (or another LoadBalancer provider) because:
- Traefik service is type `LoadBalancer`
- Without MetalLB, the service will remain in `<pending>` state
- MetalLB automatically assigns IPs from configured pools

To use without MetalLB, change the Traefik service type to `NodePort` in `traefik.yaml`.

## License

[Include your license information here]

## Support

For issues related to:
- MCP Server functionality: [MCP documentation](https://github.com/anthropics/mcp)
- AI Security API: [Palo Alto Networks AI Security docs](https://pan.dev/ai-runtime-security/)
- Kubernetes deployment: Check the troubleshooting section above