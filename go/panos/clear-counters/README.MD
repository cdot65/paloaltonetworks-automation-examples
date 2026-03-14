# PAN-OS Security Rule Hit Counter Reset Tool

## Overview

This tool clears security rule hit counters on multiple Palo Alto Networks firewalls concurrently. It uses the [pango](https://github.com/PaloAltoNetworks/pango) Go SDK to send an operational XML API command that resets hit counts for all security rules in `vsys1`. Firewall targets are defined in a YAML inventory file, and each firewall is processed in parallel using goroutines. Results are logged to the terminal.

## Prerequisites

- Go 1.18 or later
- Network access to one or more PAN-OS firewalls (HTTPS, port 443)
- Valid admin credentials for each firewall
- `gopkg.in/yaml.v2` and `github.com/PaloAltoNetworks/pango` Go modules

Generate an API key with:

```bash
curl -k 'https://192.168.1.1/api/?type=keygen&user=admin&password=your-password'
```

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/go/panos/clear-counters
   ```

2. Download dependencies:
   ```bash
   go mod download
   ```

3. Edit `firewalls.yaml` with your firewall details (see Configuration below).

4. Run the tool:
   ```bash
   go run main.go
   ```

> **`go run` vs `go build`:** `go run` compiles and runs in one step. `go build` creates a standalone binary you can copy anywhere.

## Configuration

Create or edit `firewalls.yaml` in the project directory:

```yaml
firewalls:
  - hostname: "firewall1.example.com"
    username: "admin"
    password: "your-password"

  - hostname: "firewall2.example.com"
    username: "admin"
    password: "your-password"
```

The `api_key` field is also supported in the struct but the current code authenticates with username/password.

> **Security note:** Do not commit `firewalls.yaml` with real credentials to version control. Add it to `.gitignore`.

## Usage

### Basic run

```bash
go run main.go
```

There are no command-line flags. All configuration comes from `firewalls.yaml`.

### Expected Output

```
2024/01/15 10:30:45 Initializing client for firewall1.example.com
2024/01/15 10:30:45 Initializing client for firewall2.example.com
2024/01/15 10:30:46 Client initialized for firewall1.example.com
2024/01/15 10:30:46 Sending command to firewall1.example.com
2024/01/15 10:30:46 Client initialized for firewall2.example.com
2024/01/15 10:30:46 Sending command to firewall2.example.com
2024/01/15 10:30:47 Received response from firewall1.example.com
2024/01/15 10:30:47 Successfully cleared counters on firewall1.example.com
2024/01/15 10:30:47 Received response from firewall2.example.com
2024/01/15 10:30:47 Successfully cleared counters on firewall2.example.com
```

If a firewall is unreachable:

```
2024/01/15 10:30:50 Failed to clear counter on firewall3.example.com: failed to initialize client: ...
```

The tool clears all security rule hit counters in `vsys1`. After running, the hit count columns in the firewall's security policy will reset to zero.

## Project Structure

```
clear-counters/
├── main.go              # Main application — YAML config loading, goroutine dispatch, API calls
├── firewalls.yaml       # Inventory of target firewalls with credentials
├── screenshots/         # Reference screenshots
│   ├── screenshot1.png
│   ├── screenshot2.png
│   └── screenshot3.png
└── README.md            # This file
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `connection refused` | Firewall unreachable on port 443 | Verify hostname/IP and network path |
| `failed to initialize client` | Invalid credentials | Check username/password in `firewalls.yaml` |
| `x509: certificate signed by unknown authority` | Self-signed TLS cert on firewall | pango skips verification by default; check Go TLS settings |
| `module not found` | Dependencies not downloaded | Run `go mod download` or `go mod tidy` |
| `context deadline exceeded` | Firewall API timed out | Check firewall load and network latency |
| `Failed to read file` | `firewalls.yaml` missing or unreadable | Ensure the file exists in the working directory |
| `operation failed` | API returned non-success status | Verify the user has operational command permissions |

## Go Concepts Used

| Concept | Description |
|---------|-------------|
| `go.mod` | Declares module path and dependencies |
| `go run` | Compiles and executes a Go source file in one step |
| `go build` | Compiles source into a standalone binary |
| `go mod download` | Downloads module dependencies to the local cache |
| Goroutines | Lightweight concurrent threads -- each firewall is processed in its own goroutine via `go func()` |
| `sync.WaitGroup` | Coordinates goroutine completion -- `wg.Wait()` blocks until all firewalls finish |
| Struct tags | YAML (`yaml:"hostname"`) and XML (`xml:"status,attr"`) tags control serialization/deserialization |
