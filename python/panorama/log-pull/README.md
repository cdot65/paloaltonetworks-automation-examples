# Panorama Log Retrieval and CSV Conversion

## Overview

A two-script toolkit that pulls traffic logs from Palo Alto Networks Panorama second-by-second over a configurable time range, saves raw XML responses, and converts them to CSV. The `log-pull-per-second.py` script queries the Panorama XML API directly via HTTP requests (using the `requests` library and `python-dotenv` for configuration), submitting async log jobs and polling until completion. The `xml_to_csv_converter.py` script converts the saved XML files into CSV format using a comprehensive 100+ column field mapping covering all PAN-OS traffic log fields including SD-WAN, device profiling, and container metadata.

## Prerequisites

- Python 3.11+
- uv (or pip)
- Access to a Palo Alto Networks Panorama appliance
- A Panorama API key

## Quickstart

1. Clone the repository:

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/panorama/log-pull
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```

   > **What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python, preventing version conflicts between projects.

3. Install dependencies:

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   pip install requests urllib3 python-dotenv
   ```

4. Configure credentials:

   ```bash
   cp .env.example .env
   # Edit .env with your Panorama hostname, API key, and time range
   ```

5. Pull logs:

   ```bash
   python log-pull-per-second.py
   ```

6. Convert to CSV:

   ```bash
   python xml_to_csv_converter.py
   ```

## Configuration

Copy `.env.example` to `.env` and populate with your values:

```env
PANORAMA_HOSTNAME=panorama.example.com
PANORAMA_API_KEY=your-api-key-here
START_TIME=2025/11/06 18:00:00
END_TIME=2025/11/06 19:00:00
LOG_TYPE=traffic
MAX_LOGS=5000
OUTPUT_DIR=./panorama_logs
POLL_INTERVAL=2
MAX_POLL_ATTEMPTS=60
DEBUG=false
XML_INPUT_DIR=./panorama_logs
CSV_OUTPUT_DIR=./panorama_csv
CREATE_INDIVIDUAL_CSV=true
```

| Variable | Required | Description |
|---|---|---|
| `PANORAMA_HOSTNAME` | Yes | Panorama FQDN or IP address |
| `PANORAMA_API_KEY` | Yes | API key for authentication |
| `START_TIME` | Yes | Query window start (`YYYY/MM/DD HH:MM:SS`) |
| `END_TIME` | Yes | Query window end (`YYYY/MM/DD HH:MM:SS`) |
| `LOG_TYPE` | No | PAN-OS log type: `traffic`, `threat`, `url`, etc. (default: `traffic`) |
| `MAX_LOGS` | No | Max logs per query; triggers limit detection (default: `5000`) |
| `OUTPUT_DIR` | No | Directory for XML output (default: `./panorama_logs`) |
| `REVISIT_FILE` | No | Filename for limit-hit queries (default: `revisit_manually.md`) |
| `POLL_INTERVAL` | No | Seconds between job status polls (default: `2`) |
| `MAX_POLL_ATTEMPTS` | No | Max poll attempts per job before timeout (default: `60`) |
| `DEBUG` | No | Enable debug logging (default: `false`) |
| `XML_INPUT_DIR` | No | XML source directory for converter (default: `./panorama_logs`) |
| `CSV_OUTPUT_DIR` | No | CSV output directory (default: `./panorama_csv`) |
| `CREATE_INDIVIDUAL_CSV` | No | `true` for one CSV per XML file, `false` for combined (default: `true`) |

**Security note:** Never commit your `.env` file containing real credentials to version control. The `.env.example` file contains only placeholder values.

## Usage

Pull logs from Panorama for the configured time range:

```bash
python log-pull-per-second.py
```

Convert saved XML logs to CSV:

```bash
python xml_to_csv_converter.py
```

Pull and convert in one command:

```bash
python log-pull-per-second.py && python xml_to_csv_converter.py
```

### Expected Output

Log retrieval output:

```
2025-03-14 10:00:00 - INFO - ================================================================================
2025-03-14 10:00:00 - INFO - Panorama Log Retrieval Script
2025-03-14 10:00:00 - INFO - ================================================================================
2025-03-14 10:00:00 - INFO - Output directory: ./panorama_logs
2025-03-14 10:00:00 - INFO - Time range: 2025/11/06 18:00:00 to 2025/11/06 18:05:00
2025-03-14 10:00:00 - INFO - Log type: traffic
2025-03-14 10:00:00 - INFO - Max logs per query: 5000
2025-03-14 10:00:00 - INFO - Total queries to process: 300
2025-03-14 10:00:01 - INFO - [1/300] Processing: 2025/11/06 18:00:00
2025-03-14 10:00:01 - INFO - Query submitted. Job ID: 4521
2025-03-14 10:00:03 - INFO - Job 4521 completed successfully (100% progress)
2025-03-14 10:00:03 - INFO - Saved to: ./panorama_logs/logs_20251106_180000.xml
...
2025-03-14 10:15:00 - INFO - PROCESSING COMPLETE
2025-03-14 10:15:00 - INFO - Total queries: 300
2025-03-14 10:15:00 - INFO - Successful: 298
2025-03-14 10:15:00 - INFO - Failed: 2
2025-03-14 10:15:00 - INFO - Queries requiring manual review: 1
2025-03-14 10:15:00 - INFO - Total incomplete progress polls: 5
```

CSV conversion output:

```
2025-03-14 10:20:00 - INFO - ================================================================================
2025-03-14 10:20:00 - INFO - Panorama XML to CSV Converter
2025-03-14 10:20:00 - INFO - ================================================================================
2025-03-14 10:20:00 - INFO - CSV output directory: ./panorama_csv
2025-03-14 10:20:00 - INFO - Found 298 XML files to process
2025-03-14 10:20:00 - INFO - Mode: Individual CSV files
2025-03-14 10:20:01 - INFO - [1/298] Processing: logs_20251106_180000.xml
2025-03-14 10:20:01 - INFO - Parsed 42 entries from logs_20251106_180000.xml
2025-03-14 10:20:01 - INFO - Created: ./panorama_csv/logs_20251106_180000.csv
...
2025-03-14 10:20:30 - INFO - CONVERSION COMPLETE
```

The log retrieval script queries one second at a time, submits async jobs, and polls until complete. Queries hitting the 5000-log limit are flagged in `revisit_manually.md` for manual review with refined filters.

## Project Structure

```
log-pull/
├── log-pull-per-second.py      # Log retrieval script (second-by-second queries)
├── xml_to_csv_converter.py     # XML-to-CSV converter with full field mapping
├── pyproject.toml              # Project metadata and dependencies (uv/pip)
├── .env.example                # Environment variable template
├── panorama_logs/              # Raw XML output (created at runtime)
└── panorama_csv/               # CSV output (created at runtime)
```

## Troubleshooting

| Problem | Solution |
|---|---|
| Connection refused | Verify `PANORAMA_HOSTNAME` is correct and Panorama is reachable on port 443 |
| Invalid credentials / 403 | Regenerate your API key in Panorama and update `.env` |
| ModuleNotFoundError | Run `uv sync` or `pip install requests urllib3 python-dotenv` |
| SSL certificate verification error | The script disables SSL warnings by default; ensure Panorama is accessible via HTTPS |
| Timeout / `Job timed out after 60 attempts` | Increase `MAX_POLL_ATTEMPTS` or `POLL_INTERVAL` in `.env` |
| `Please configure your API key` | Edit `.env` and replace the placeholder `your-api-key-here` with your actual key |
| `No XML files found` | Run `log-pull-per-second.py` first to generate XML files before running the converter |
| `Queries requiring manual review` | Check `revisit_manually.md`; these time slices had 5000+ logs and need finer query filters |
