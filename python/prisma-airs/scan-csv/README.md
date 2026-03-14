# Prisma AIRS CSV Prompt Scanner

## Overview

A Python script that reads prompts from a CSV file and scans each one synchronously through the Palo Alto Networks AI Runtime Security (AIRS) API using direct HTTP requests. It sends each prompt to the AIRS sync scan endpoint with configurable retry logic, and writes results including action (allow/block), category, scan ID, round-trip time, and HTTP status code to an output CSV. Configuration is loaded from a TOML file.

## Prerequisites

- Python 3.11+ (uses `tomllib` from the standard library)
- A Palo Alto Networks AI Runtime Security API key
- An AIRS AI Profile ID

## Quickstart

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/prisma-airs/scan-csv
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   > **Tip -- What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python. This prevents version conflicts between projects.

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure credentials:**

   Create a `config.toml` file with your API key and profile ID (see Configuration below).

5. **Run the scanner:**

   ```bash
   python scan.py
   ```

## Configuration

Create a `config.toml` file in the project root:

```toml
api_key = "your-api-key-here"
profile_id = "your-profile-id-here"
input_csv = "test-prompts.csv"
output_csv = "prompts_and_results.csv"

[api]
endpoint = "https://service.api.aisecurity.paloaltonetworks.com/v1/scan/sync/request"
max_retries = 3
retry_delay = 1

[logging]
level = "INFO"
format = "%(asctime)s - %(levelname)s - %(message)s"
```

| Variable | Required | Description |
|---|---|---|
| `api_key` | Yes | Your AIRS API key |
| `profile_id` | Yes | AI Profile UUID |
| `input_csv` | No | Path to input CSV (default: `prompts.csv`) |
| `output_csv` | No | Path to output CSV (default: `prompts_and_results.csv`) |
| `api.endpoint` | No | AIRS sync scan endpoint URL |
| `api.max_retries` | No | Number of retry attempts for 4xx errors (default: 3) |
| `api.retry_delay` | No | Seconds between retries (default: 1) |
| `logging.level` | No | Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL |

**Security note:** Never commit `config.toml` with real API keys to version control.

## Usage

**Run with the default config file:**

```bash
python scan.py
```

**Specify a custom config file:**

```bash
python scan.py --config my-config.toml
```

The input CSV should contain one prompt per row in the first column. See `test-prompts.csv` for an example with prompts like "What is the capital of France?" and "How do I make a paper airplane?".

### Expected Output

Console output during scanning:

```
2024-01-15 14:30:22 - INFO - Starting prompt processing from 'test-prompts.csv' with profile ID '32e7ce92-...'
2024-01-15 14:30:22 - INFO - Configuration loaded from: config.toml
2024-01-15 14:30:22 - INFO - Processing started at 2024-01-15 14:30:22
2024-01-15 14:30:22 - INFO - Processing row 1: What is the capital of France?...
2024-01-15 14:30:23 - INFO - Row 1 processed successfully (Status: 200)
2024-01-15 14:30:23 - INFO - Processing row 2: How do I make a paper airplane?...
2024-01-15 14:30:23 - INFO - Row 2 processed successfully (Status: 200)
...
2024-01-15 14:30:30 - INFO - Processing complete! Results saved to 'prompts_and_results.csv'
2024-01-15 14:30:30 - INFO - Processing ended at 2024-01-15 14:30:30
2024-01-15 14:30:30 - INFO - Total execution time: 8.45 seconds (0.14 minutes)
```

The output CSV (`prompts_and_results.csv`) contains columns: `prompt`, `action`, `category`, `scan_id`, `report_id`, `profile_name`, `round_trip`, `status_code`.

## Project Structure

```
scan-csv/
  scan.py            # Main script with scan logic, retry handling, and CSV I/O
  config.toml        # TOML configuration file (API key, profile, endpoints)
  test-prompts.csv   # Sample input prompts (10 benign prompts)
  requirements.txt   # Dependencies (requests)
```

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `Error: Configuration file 'config.toml' not found` | Missing config file | Create `config.toml` with required fields |
| `API key not configured` | Empty `api_key` in config | Set `api_key` in `config.toml` |
| `ModuleNotFoundError: No module named 'requests'` | Dependencies not installed | Run `pip install -r requirements.txt` |
| SSL certificate verify failed | Corporate proxy or outdated certs | Update CA certificates or set `verify=False` in requests (not recommended) |
| Connection timeout on API requests | Network issues or API downtime | Check connectivity; increase `api.max_retries` and `api.retry_delay` in config |
| `CSV file 'prompts.csv' not found` | Input file path incorrect | Set `input_csv` in config to the correct path |
| HTTP 401 status on requests | Invalid API key | Verify `api_key` in `config.toml` is correct and active |
