# PAN-OS Global Counter Collection Tool

## Overview

This tool retrieves global counters from multiple Palo Alto Networks firewalls concurrently and saves the results as YAML files. It uses the [pango](https://github.com/PaloAltoNetworks/pango) Go SDK to send the `<show><counter><global/></counter></show>` operational command via the XML API. Each firewall is queried in parallel using goroutines, and counter data (packet stats, flow metrics, device info) is written to individual YAML files in an `output/` directory.

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
   cd paloaltonetworks-automation-examples/go/panos/get-counters
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

> **Security note:** Do not commit `firewalls.yaml` with real credentials to version control. Add it to `.gitignore`.

## Usage

### Basic run

```bash
go run main.go
```

There are no command-line flags. All configuration comes from `firewalls.yaml`.

### Expected Output

Terminal output:

```
2024/01/15 10:30:45 Initializing client for firewall1.example.com
2024/01/15 10:30:45 Initializing client for firewall2.example.com
2024/01/15 10:30:46 Client initialized for firewall1.example.com
2024/01/15 10:30:46 Sending command to firewall1.example.com
2024/01/15 10:30:47 Received response from firewall1.example.com
2024/01/15 10:30:47 Response written to output/firewall1.yaml
2024/01/15 10:30:47 Client initialized for firewall2.example.com
2024/01/15 10:30:47 Sending command to firewall2.example.com
2024/01/15 10:30:48 Received response from firewall2.example.com
2024/01/15 10:30:48 Response written to output/firewall2.yaml
```

Each output YAML file contains the parsed counter data:

```yaml
status: success
result:
  global:
    t: 113169
    counters:
      entries:
      - category: packet
        name: pkt_recv
        value: 594545
        rate: 2
        aspect: pktproc
        desc: Packets received
        id: 17
        severity: info
      - category: flow
        name: flow_arp_pkt_rcv
        value: 47358
        rate: 0
        aspect: arp
        desc: ARP packets received
        id: 1078
        severity: info
```

Output files are named after the firewall hostname (without domain), e.g., `output/firewall1.yaml`. The `output/` directory is created automatically if it does not exist.

## Project Structure

```
get-counters/
├── main.go              # Main application — YAML config, goroutine dispatch, API calls, file output
├── firewalls.yaml       # Inventory of target firewalls with credentials
├── output/              # Generated YAML files (one per firewall)
│   ├── austin-fw1.yaml
│   ├── dallas-fw1.yaml
│   └── ...
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
| `Failed to create output directory` | Permissions issue | Check write permissions in the project directory |
| `failed to unmarshal response` | Unexpected XML response format | Verify PAN-OS version compatibility |

## Go Concepts Used

| Concept | Description |
|---------|-------------|
| `go.mod` | Declares module path and dependencies |
| `go run` | Compiles and executes a Go source file in one step |
| `go build` | Compiles source into a standalone binary |
| `go mod download` | Downloads module dependencies to the local cache |
| Goroutines | Lightweight concurrent threads -- each firewall is queried in its own goroutine |
| `sync.WaitGroup` | Coordinates goroutine completion -- blocks until all firewalls are processed |
| Struct tags | YAML (`yaml:"hostname"`) and XML (`xml:"category"`) tags control serialization/deserialization |
