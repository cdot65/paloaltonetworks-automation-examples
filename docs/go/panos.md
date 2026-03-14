# PAN-OS Go Tools

2 Go CLI tools for PAN-OS firewall operations.

## Projects

### Commit Tool

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/go/panos/commit)

Uses the `pango` SDK to execute and wait for configuration commits on a PAN-OS firewall. Supports partial commits, forced commits, admin-scoped commits, and commit descriptions via CLI flags.

**CLI Flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `-hostname` | | Firewall IP or hostname |
| `-username` | | Admin username |
| `-password` | | Admin password |
| `-description` | | Commit description |
| `-force` | `false` | Force commit even without changes |
| `-partial` | `false` | Partial commit for current admin only |

**Example:**

```bash
go run main.go -hostname 192.168.1.1 -username admin -password your-password -description "Add new address objects"
```

---

### Session Analyzer

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/go/panos/session-analyzer)

Queries PAN-OS for all active sessions via the XML API and filters for sessions older than a configurable age threshold. Reports source, destination, application, state, and byte count for long-running sessions.

**Example:**

```bash
go run main.go -hostname 192.168.1.1 -api-key your-api-key -age 3600
```
