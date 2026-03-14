# PAN-OS Firewall Commit Tool

## Overview

This tool performs configuration commits on a Palo Alto Networks firewall using the PAN-OS XML API. It uses the [pango](https://github.com/PaloAltoNetworks/pango) Go SDK to connect to a firewall, execute a commit operation, and wait for job completion. The tool supports partial commits, forced commits, admin-scoped commits, and commit descriptions, all controlled via command-line flags. Output is logged to the terminal with timestamps.

## Prerequisites

- Go 1.18 or later
- Network access to a PAN-OS firewall (HTTPS, port 443)
- A valid PAN-OS admin username/password or API key

Generate an API key with:

```bash
curl -k 'https://192.168.1.1/api/?type=keygen&user=admin&password=your-password'
```

## Quickstart

1. Clone the repository:
   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/go/panos/commit
   ```

2. Download dependencies:
   ```bash
   go mod download
   ```

3. Run the tool:
   ```bash
   go run firewall-commit.go -host 192.168.1.1 -user admin -pass your-password "My commit description"
   ```

> **`go run` vs `go build`:** `go run` compiles and runs in one step. `go build` creates a standalone binary you can copy anywhere.

## Configuration

This tool uses command-line flags exclusively (no config file required). Alternatively, you can supply a JSON config file with `-config`.

### Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-config` | `""` | JSON config file with PAN-OS connection info |
| `-host` | `""` | PAN-OS firewall hostname or IP |
| `-user` | `""` | PAN-OS username |
| `-pass` | `""` | PAN-OS password |
| `-key` | `""` | PAN-OS API key (alternative to user/pass) |
| `-admins` | `""` | CSV of admin names for partial commit |
| `-exclude-device-and-network` | `false` | Exclude device and network config from commit |
| `-exclude-shared-objects` | `false` | Exclude shared objects from commit |
| `-exclude-policy-and-objects` | `false` | Exclude policy and objects from commit |
| `-force` | `false` | Force commit even if no changes are pending |
| `-sleep` | `1` | Seconds between job completion checks |
| `-timeout` | `10` | Timeout in seconds for PAN-OS API calls |

The commit description is passed as a positional argument after all flags.

> **Security note:** Do not hardcode credentials in scripts or commit them to git. Use environment variables or a config file excluded via `.gitignore`.

## Usage

### Basic commit

```bash
go run firewall-commit.go -host 192.168.1.1 -user admin -pass your-password
```

### Commit with description and API key

```bash
go run firewall-commit.go -host 192.168.1.1 -key LUFRPT1EXAMPLE "Updated security rules"
```

### Partial commit for specific admins

```bash
go run firewall-commit.go -host 192.168.1.1 -user admin -pass your-password \
  -admins "admin1,admin2" -exclude-shared-objects
```

### Force commit with custom timeout

```bash
go run firewall-commit.go -host 192.168.1.1 -key LUFRPT1EXAMPLE -force -timeout 30
```

### Expected Output

```
2024/01/15 10:30:45.123456 Committed config successfully
```

If no changes are pending:

```
2024/01/15 10:30:45.123456 No commit needed
```

If the commit fails:

```
2024/01/15 10:30:45.123456 Error in commit: <error details>
```

The tool exits with a non-zero status code on failure.

## Project Structure

```
commit/
├── firewall-commit.go   # Main application — flag parsing, pango client init, commit logic
└── README.md            # This file
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `connection refused` | Firewall unreachable on port 443 | Verify hostname/IP and network connectivity |
| `Failed: invalid credentials` | Wrong username/password or API key | Regenerate API key or check credentials |
| `x509: certificate signed by unknown authority` | Self-signed TLS certificate | The pango library skips TLS verification by default; check firewall cert config |
| `module not found` | Missing Go dependencies | Run `go mod download` or `go mod tidy` |
| `context deadline exceeded` | API call timed out | Increase `-timeout` value |
| `No commit needed` | No pending configuration changes | Use `-force` to commit anyway |
| `Error in commit: commit is in progress` | Another commit is running | Wait for the existing commit to finish |

## Go Concepts Used

| Concept | Description |
|---------|-------------|
| `go.mod` | Declares module path and dependencies (requires initialization with `go mod init`) |
| `go run` | Compiles and executes a Go source file in one step |
| `go build` | Compiles source into a standalone binary |
| `go mod download` | Downloads module dependencies to the local cache |
| `flag` package | Standard library for parsing command-line flags |
| Struct tags | Metadata on struct fields used for serialization |
