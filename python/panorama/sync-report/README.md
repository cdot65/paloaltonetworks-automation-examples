# Panorama Sync Status Report

## Overview

A script that checks the synchronization status of device groups and templates on Palo Alto Networks Panorama and generates a color-coded PDF report. It queries the Panorama XML API directly via HTTP requests (using the `requests` library), parses XML responses with `xmltodict`, and renders results into a PDF using ReportLab. In-sync items appear in green and out-of-sync items in red, providing a quick visual audit of configuration push status. Settings are managed with Dynaconf.

## Prerequisites

- Python 3.11+
- pip
- Access to a Palo Alto Networks Panorama appliance
- A Panorama API key

## Quickstart

1. Clone the repository:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/panorama/sync-report
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```

   > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python, preventing version conflicts between projects.

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure credentials by creating a `.secrets.yaml` file:

   ```yaml
   hostname: "panorama.example.com"
   api_key: "your-api-key-here"
   ```

5. Run the tool:

   ```bash
   python app.py
   ```

## Configuration

Create a `.secrets.yaml` file with Panorama credentials:

```yaml
hostname: "panorama.example.com"
api_key: "your-api-key-here"
```

| Variable | Required | Description |
|---|---|---|
| `hostname` | Yes | Panorama FQDN or IP address (in `.secrets.yaml`) |
| `api_key` | Yes | API key for authentication (in `.secrets.yaml`) |

Alternatively, set environment variables with the `DYNACONF_` prefix (e.g., `DYNACONF_HOSTNAME`, `DYNACONF_API_KEY`).

**Security note:** Never commit `.secrets.yaml` to version control. Add it to your `.gitignore`.

## Usage

Generate sync report with default filename:

```bash
python app.py
```

Specify output filename:

```bash
python app.py --output my_report.pdf
```

Enable debug logging:

```bash
python app.py --debug
```

| Flag | Description |
|---|---|
| `-o`, `--output` | Output PDF file name (default: `panorama_sync_report.pdf`) |
| `-d`, `--debug` | Enable debug-level logging |

### Expected Output

Console output:

```
2025-03-14 10:00:01 - __main__ - INFO - Script execution started.
2025-03-14 10:00:01 - __main__ - INFO - Retrieving data from panorama.example.com
2025-03-14 10:00:02 - __main__ - INFO - Retrieving data from panorama.example.com
2025-03-14 10:00:03 - __main__ - INFO - PDF report generated: /path/to/panorama_sync_report.pdf
2025-03-14 10:00:03 - __main__ - INFO - Script execution completed.
```

The generated PDF contains two tables: one for device groups and one for templates. Each row shows the name and sync status ("In Sync" in green or "Out of Sync" in red). A log file `panorama_sync_check.log` is also created.

## Project Structure

```
sync-report/
├── app.py              # Main script: API queries, sync parsing, PDF generation
├── config.py           # Dynaconf settings loader
├── settings.yaml       # Placeholder for additional settings
├── .secrets.yaml       # Panorama credentials (do not commit)
└── requirements.txt    # Python dependencies (requests, reportlab, xmltodict, etc.)
```

## Troubleshooting

| Problem | Solution |
|---|---|
| Connection refused | Verify `hostname` in `.secrets.yaml` is correct and Panorama is reachable on port 443 |
| Invalid credentials / 403 | Regenerate your API key in Panorama and update `.secrets.yaml` |
| ModuleNotFoundError | Run `pip install -r requirements.txt` to install all dependencies |
| SSL certificate verification error | The script disables SSL warnings by default; ensure Panorama is accessible via HTTPS |
| Timeout retrieving data | Check network connectivity to Panorama; large deployments may take longer |
| `KeyError: 'devicegroups'` | Panorama returned an unexpected XML structure; verify API access and Panorama version |
| Empty PDF tables | Panorama may have no device groups or templates configured |
