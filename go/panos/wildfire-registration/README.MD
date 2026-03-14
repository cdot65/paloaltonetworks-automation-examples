# PAN-OS WildFire Public Cloud Registration Tool

## Overview

This tool registers Palo Alto Networks firewalls with the WildFire Public Cloud service. It can discover managed firewalls through Panorama's XML API or use a static inventory file. The tool connects to each firewall via SSH using [scrapligo](https://github.com/scrapli/scrapligo) and executes `request wildfire registration channel public`. It uses [pango](https://github.com/PaloAltoNetworks/pango) for Panorama device discovery and supports concurrent operations with configurable parallelism, hostname filtering, and debug logging.

## Prerequisites

- Go 1.18 or later
- Network access to Panorama (HTTPS, port 443) and/or firewalls (SSH, port 22)
- Valid admin credentials for Panorama and firewalls
- `gopkg.in/yaml.v2`, `github.com/PaloAltoNetworks/pango`, and `github.com/scrapli/scrapligo` Go modules

Generate an API key with:

```bash
curl -k 'https://192.168.1.1/api/?type=keygen&user=admin&password=your-password'
```

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/go/panos/wildfire-registration
   ```

2. Download dependencies:
   ```bash
   go mod download
   ```

3. Edit the configuration files (see Configuration below).

4. Run the tool:
   ```bash
   go run main.go
   ```

> **`go run` vs `go build`:** `go run` compiles and runs in one step. `go build` creates a standalone binary you can copy anywhere.

## Configuration

### Panorama config (`panorama.yaml`)

```yaml
panorama:
  - hostname: "panorama.example.com"
```

### Secrets file (`.secrets.yaml`)

```yaml
auth:
  panorama:
    username: "your-panorama-username"
    password: "your-panorama-password"
  firewall:
    username: "your-firewall-username"
    password: "your-firewall-password"
```

### Static inventory (`inventory.yaml`) -- used with `-nopanorama` flag

```yaml
inventory:
  - hostname: "fw1"
    ip_address: "192.168.1.1"
  - hostname: "fw2"
    ip_address: "192.168.1.2"
```

> **Security note:** Add `.secrets.yaml` to `.gitignore`. Never commit credentials to version control.

### Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-debug` | `0` | Debug level: 0=INFO, 1=DEBUG |
| `-concurrency` | CPU count | Number of concurrent SSH operations |
| `-config` | `panorama.yaml` | Path to the Panorama configuration file |
| `-secrets` | `.secrets.yaml` | Path to the secrets file |
| `-filter` | `""` | Comma-separated hostname patterns to filter devices |
| `-verbose` | `false` | Enable verbose (debug) logging |
| `-nopanorama` | `false` | Use `inventory.yaml` instead of querying Panorama |

## Usage

### Discover devices from Panorama and register all

```bash
go run main.go
```

### Use static inventory (no Panorama)

```bash
go run main.go -nopanorama
```

### Filter to specific firewalls

```bash
go run main.go -filter "austin,dallas"
```

### Verbose output with limited concurrency

```bash
go run main.go -verbose -concurrency 2
```

### Expected Output

```
Device List:
Device 1:
  hostname: austin-fw1
  ip-address: 10.0.1.1
  serial: 0123456789
  model: PA-450

Device 2:
  hostname: dallas-fw1
  ip-address: 10.0.2.1
  serial: 9876543210
  model: PA-850

WildFire Registration Results:
austin-fw1: Successfully registered WildFire
dallas-fw1: Successfully registered WildFire
```

With `-verbose`:

```
2024/01/15 10:30:45 [INFO] Initializing client for panorama.example.com
2024/01/15 10:30:46 [INFO] Client initialized for panorama.example.com
2024/01/15 10:30:46 [INFO] Filtered devices: 2 out of 10
2024/01/15 10:30:46 [INFO] Starting WildFire registration for 2 devices
2024/01/15 10:30:46 [DEBUG] Attempting to connect to austin-fw1 at 10.0.1.1
2024/01/15 10:30:47 [DEBUG] Successfully connected to austin-fw1
2024/01/15 10:30:47 [DEBUG] Sending WildFire registration command to austin-fw1
2024/01/15 10:30:48 [INFO] Registration complete. Successes: 2, Failures: 0
```

A final summary line reports the total number of successful and failed registrations.

## Project Structure

```
wildfire-registration/
├── main.go              # Main application — Panorama discovery, SSH registration, concurrency
├── panorama.yaml        # Panorama connection config
├── .secrets.yaml        # Credentials for Panorama and firewalls (do not commit)
├── inventory.yaml       # Static device inventory (alternative to Panorama discovery)
├── screenshots/         # Reference screenshots
│   ├── screenshot1.png
│   ├── screenshot2.png
│   ├── screenshot3.png
│   └── screenshot4.png
└── README.md            # This file
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `connection refused` (port 443) | Panorama unreachable | Verify Panorama hostname and network access |
| `connection refused` (port 22) | Firewall SSH unreachable | Check firewall SSH access and management profile |
| `failed to initialize client` | Invalid Panorama credentials | Check `.secrets.yaml` Panorama section |
| `failed to open connection` | SSH auth failure to firewall | Check `.secrets.yaml` firewall credentials |
| `x509: certificate signed by unknown authority` | Self-signed TLS cert | pango skips TLS verification by default |
| `module not found` | Dependencies not downloaded | Run `go mod download` or `go mod tidy` |
| `Timeout waiting for result` | Firewall did not respond within 6 minutes | Check firewall load and SSH connectivity |
| `unexpected command output` | WildFire registration command returned unexpected text | Verify PAN-OS version supports the command |
| `No Panorama configuration found` | Empty or malformed `panorama.yaml` | Check YAML syntax and structure |

## Go Concepts Used

| Concept | Description |
|---------|-------------|
| `go.mod` | Declares module path and dependencies |
| `go run` | Compiles and executes a Go source file in one step |
| `go build` | Compiles source into a standalone binary |
| `go mod download` | Downloads module dependencies to the local cache |
| Goroutines | Concurrent execution -- each device registration runs in its own goroutine |
| `sync.WaitGroup` | Coordinates goroutine completion |
| Channels | `results` channel collects outcomes; `sem` channel acts as a semaphore for concurrency limiting |
| Struct tags | YAML and XML struct tags for config and API response parsing |
