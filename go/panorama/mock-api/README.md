# Panorama Mock API Server

## Overview

This is a placeholder project intended to provide a mock Palo Alto Networks Panorama API server for testing and development purposes. The project currently contains only dependency metadata (`go.sum`) with no implemented Go source code. It is based on the [Gin](https://github.com/gin-gonic/gin) web framework, as indicated by the dependency list. No functional code exists yet.

## Prerequisites

- Go 1.18 or later

Generate an API key (for reference when the mock is implemented):

```bash
curl -k 'https://192.168.1.1/api/?type=keygen&user=admin&password=your-password'
```

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/go/panorama/mock-api
   ```

2. Download dependencies:
   ```bash
   go mod download
   ```

3. **Note:** There is no `main.go` or runnable source code yet. This project is a stub.

> **`go run` vs `go build`:** `go run` compiles and runs in one step. `go build` creates a standalone binary you can copy anywhere.

## Configuration

No configuration files exist yet. When implemented, the server will likely accept settings for bind address, port, and mock response data.

> **Security note:** Keep any future credentials or API keys out of version control.

## Usage

This project is not yet functional. When implemented, the expected usage would be:

```bash
go run main.go
```

### Expected Output

Not yet available. The planned Gin-based server would output something like:

```
[GIN-debug] Listening and serving HTTP on :8080
```

## Project Structure

```
mock-api/
├── go.sum               # Dependency checksums (Gin framework and transitive deps)
└── README.md            # This file
```

**Status:** Placeholder -- no source code implemented. The `go.sum` indicates planned use of `gin-gonic/gin v1.10.0` as the HTTP framework.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `connection refused` | Server not running or wrong port | Start the server and check the bind address |
| `invalid credentials` | Not applicable yet | Will depend on implementation |
| `x509: certificate signed by unknown authority` | TLS not configured | Configure TLS or use HTTP for local testing |
| `module not found` | Missing go.mod or dependencies | Run `go mod init` then `go mod tidy` |
| `context deadline exceeded` | Server not responding | Check if the server process is running |

## Go Concepts Used

| Concept | Description |
|---------|-------------|
| `go.mod` | Declares module path and dependencies (needs to be created with `go mod init`) |
| `go.sum` | Records cryptographic checksums of dependencies |
| `go run` | Compiles and executes a Go source file in one step |
| `go build` | Compiles source into a standalone binary |
| `go mod download` | Downloads module dependencies to the local cache |
