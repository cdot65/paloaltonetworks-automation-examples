# Event-Driven Ansible

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/ansible/event-driven-ansible)

A containerized Event-Driven Ansible (EDA) environment that listens for PAN-OS log events via HTTP Server Profiles and triggers automated remediation playbooks.

## How It Works

```mermaid
graph LR
    A[PAN-OS Firewall] -->|HTTP Server Profile| B[EDA Container :5000]
    B -->|Rulebook Match| C[Remediation Playbook]
    C -->|API Call| D[AAP / Direct Execution]
```

1. PAN-OS sends log events to the EDA container via HTTP Server Profiles on port 5000
2. EDA rulebooks evaluate incoming events against defined conditions
3. Matching events trigger remediation playbooks for decryption issues, DLP violations, or system log events
4. Playbooks execute remediation actions (TLS certificate deployment, Slack alerts, ServiceNow tickets)

## Container Image

The Dockerfile builds a container with:

- `ansible-rulebook` for event-driven automation
- `aiohttp` for the HTTP event source
- Pre-loaded rulebooks and playbooks

## Supported Event Types

| Log Type | Trigger | Remediation |
|----------|---------|-------------|
| Decryption | TLS certificate errors | Certificate push to endpoints |
| DLP | Data loss prevention violations | Slack notification |
| System | System log events | ServiceNow ticket creation |
