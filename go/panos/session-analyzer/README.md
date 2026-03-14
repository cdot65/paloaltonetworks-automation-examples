# PAN-OS Long-Running Session Analyzer

## Overview

This tool identifies long-running sessions on a Palo Alto Networks firewall by querying the PAN-OS XML API. It uses the [pango](https://github.com/PaloAltoNetworks/pango) Go SDK to send `<show><session><all/></session></show>`, parses the XML response, and filters sessions older than a configurable age threshold. Configuration is split between a settings file (hostname, time threshold) and a secrets file (API key). Results are printed to the terminal with details including source, destination, application, state, and byte count.

## Prerequisites

- Go 1.18 or later
- Network access to a PAN-OS firewall (HTTPS, port 443)
- A valid PAN-OS API key
- `gopkg.in/yaml.v2` and `github.com/PaloAltoNetworks/pango` Go modules

Generate an API key with:

```bash
curl -k 'https://192.168.1.1/api/?type=keygen&user=admin&password=your-password'
```

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/go/panos/session-analyzer
   ```

2. Download dependencies:
   ```bash
   go mod download
   ```

3. Edit `settings.yaml` and `.secrets.yaml` (see Configuration below).

4. Run the tool:
   ```bash
   go run main.go
   ```

> **`go run` vs `go build`:** `go run` compiles and runs in one step. `go build` creates a standalone binary you can copy anywhere.

## Configuration

### Settings file (`settings.yaml`)

```yaml
hostname: firewall.example.com
minutes: 1440   # 24 hours — sessions older than this are reported
```

### Secrets file (`.secrets.yaml`)

```yaml
api_key: LUFRPT1YOUR-API-KEY-HERE
```

> **Security note:** Add `.secrets.yaml` to `.gitignore`. Never commit API keys to version control.

## Usage

### Basic run

```bash
go run main.go
```

There are no command-line flags. All configuration comes from `settings.yaml` and `.secrets.yaml`.

### Expected Output

```
Sessions older than 1440 minutes:
------------------------------------
Session ID: 12345
  Start Time: Mon Jan 13 08:15:30 2024
  Source: 10.0.1.50
  Destination: 203.0.113.25
  Application: ssl
  State: ACTIVE
  Total Byte Count: 15728640 (15.00 MB)
------------------------------------
Session ID: 12400
  Start Time: Sun Jan 12 22:45:10 2024
  Source: 10.0.2.100
  Destination: 198.51.100.10
  Application: web-browsing
  State: ACTIVE
  Total Byte Count: 5242880 (5.00 MB)
------------------------------------
```

If no sessions exceed the threshold, only the header line is printed:

```
Sessions older than 1440 minutes:
------------------------------------
```

Each session entry shows the session ID, start time, source/destination IPs, application name, connection state, and total bytes transferred (with a human-readable MB conversion).

## Project Structure

```
session-analyzer/
├── main.go              # Main application — settings/secrets loading, API query, session filtering
├── settings.yaml        # Firewall hostname and age threshold config
├── .secrets.yaml        # API key (do not commit)
├── docs/
│   └── screenshots/
│       └── execute.png  # Reference screenshot
└── README.md            # This file
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `connection refused` | Firewall unreachable on port 443 | Verify hostname in `settings.yaml` and network access |
| `Failed to initialize client` | Invalid API key | Regenerate the API key and update `.secrets.yaml` |
| `x509: certificate signed by unknown authority` | Self-signed TLS cert | pango skips verification by default; check Go TLS config |
| `module not found` | Dependencies not downloaded | Run `go mod download` or `go mod tidy` |
| `context deadline exceeded` | API call timed out | Check firewall load; consider reducing session table size |
| `Error loading settings` | `settings.yaml` missing or malformed | Ensure the file exists with valid YAML |
| `Error loading secrets` | `.secrets.yaml` missing or malformed | Ensure the file exists with `api_key` field |
| `error parsing timestamp` | Session timestamp format mismatch | Verify PAN-OS version returns timestamps in `Mon Jan 2 15:04:05 2006` format |

## Go Concepts Used

| Concept | Description |
|---------|-------------|
| `go.mod` | Declares module path and dependencies |
| `go run` | Compiles and executes a Go source file in one step |
| `go build` | Compiles source into a standalone binary |
| `go mod download` | Downloads module dependencies to the local cache |
| Struct tags | YAML (`yaml:"hostname"`) and XML (`xml:"source"`) tags for config and response parsing |
| `time.Parse` | Parses timestamp strings into Go `time.Time` values using a reference format |
