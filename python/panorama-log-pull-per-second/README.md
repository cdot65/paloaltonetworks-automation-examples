# Panorama Log Pull Per Second

Two Python scripts to retrieve and convert Palo Alto Networks Panorama traffic logs:
1. **log-pull-per-second.py** - Queries Panorama XML API second-by-second for traffic logs
2. **xml_to_csv_converter.py** - Converts retrieved XML logs to CSV format

## Features

- Query Panorama logs with per-second granularity
- Automatic job polling and result retrieval
- Track queries hitting the 5000 log limit for manual review
- Convert XML logs to CSV with comprehensive field mapping
- Environment-based configuration
- Debug logging support
- Individual or combined CSV output modes

## Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager
- Access to Panorama with valid API key
- Network connectivity to Panorama instance

## Installation

1. Clone or navigate to project directory:
```bash
cd panorama-log-pull-per-second
```

2. Copy environment template and configure:
```bash
cp .env.example .env
```

3. Edit `.env` with your Panorama details:
```bash
# Required: Update these values
PANORAMA_HOSTNAME=your-panorama.example.com
PANORAMA_API_KEY=your-api-key-here
START_TIME=2025/11/06 18:00:00
END_TIME=2025/11/06 19:00:00
```

4. Install dependencies:
```bash
uv sync
```

## Configuration

### Environment Variables

All configuration is managed through `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `PANORAMA_HOSTNAME` | Panorama hostname/IP | `magnolia1.cdot.io` |
| `PANORAMA_API_KEY` | Panorama API key | `your-api-key-here` |
| `START_TIME` | Query start time | `2025/11/06 18:00:00` |
| `END_TIME` | Query end time | `2025/11/06 19:00:00` |
| `LOG_TYPE` | Log type to retrieve | `traffic` |
| `MAX_LOGS` | Max logs per query | `5000` |
| `OUTPUT_DIR` | XML output directory | `./panorama_logs` |
| `REVISIT_FILE` | File tracking queries at limit | `revisit_manually.md` |
| `POLL_INTERVAL` | Seconds between status checks | `2` |
| `MAX_POLL_ATTEMPTS` | Max polling attempts | `60` |
| `DEBUG` | Enable debug logging | `false` |
| `XML_INPUT_DIR` | XML input directory for converter | `./panorama_logs` |
| `CSV_OUTPUT_DIR` | CSV output directory | `./panorama_csv` |
| `CREATE_INDIVIDUAL_CSV` | Create separate CSV per XML | `true` |

### Time Format

Use format: `YYYY/MM/DD HH:MM:SS`

Example: `2025/11/06 18:15:00`

## Usage

### Step 1: Pull Logs from Panorama

Run the log retrieval script:

```bash
uv run python log-pull-per-second.py
```

**Output:**
- XML files saved to `OUTPUT_DIR` (default: `./panorama_logs`)
- One XML file per second: `logs_20251106_181500.xml`
- `revisit_manually.md` created if queries hit 5000 log limit

**Example output:**
```
2025-11-06 18:15:00 - INFO - Panorama Log Retrieval Script
2025-11-06 18:15:00 - INFO - Output directory: ./panorama_logs
2025-11-06 18:15:00 - INFO - Time range: 2025/11/06 18:00:00 to 2025/11/06 19:00:00
2025-11-06 18:15:00 - INFO - [1/3600] Processing: 2025/11/06 18:00:00
2025-11-06 18:15:00 - INFO - Query submitted. Job ID: 12345
2025-11-06 18:15:02 - INFO - Job 12345 completed successfully
2025-11-06 18:15:02 - INFO - Saved to: ./panorama_logs/logs_20251106_180000.xml
```

### Step 2: Convert XML to CSV

After retrieving logs, convert to CSV:

```bash
uv run python xml_to_csv_converter.py
```

**Output:**
- CSV files saved to `CSV_OUTPUT_DIR` (default: `./panorama_csv`)
- Individual CSV per XML (or combined if `CREATE_INDIVIDUAL_CSV=false`)

**Example output:**
```
2025-11-06 18:15:05 - INFO - Panorama XML to CSV Converter
2025-11-06 18:15:05 - INFO - Found 300 XML files to process
2025-11-06 18:15:05 - INFO - Mode: Individual CSV files
2025-11-06 18:15:05 - INFO - [1/300] Processing: logs_20251106_181500.xml
2025-11-06 18:15:05 - INFO - Parsed 26 entries from logs_20251106_181500.xml
2025-11-06 18:15:05 - INFO - Created: ./panorama_csv/logs_20251106_181500.csv
2025-11-06 18:15:10 - INFO - Total CSV files created: 181
2025-11-06 18:15:10 - INFO - Total log entries processed: 5499
```

## Debug Mode

Enable debug logging for troubleshooting:

```bash
# In .env file
DEBUG=true
```

Debug mode shows:
- Query strings submitted to Panorama
- Job polling attempts
- Detailed API responses

## Advanced Usage

### Custom Time Range

Query specific time period:

```bash
# Edit .env
START_TIME=2025/11/06 08:00:00
END_TIME=2025/11/06 08:05:00  # 5 minutes = 300 queries
```

### Different Log Types

Query other log types:

```bash
# Edit .env
LOG_TYPE=threat  # Options: threat, url, wildfire, etc.
```

### Combined CSV Output

Create single CSV with all logs:

```bash
# Edit .env
CREATE_INDIVIDUAL_CSV=false
```

Output: `./panorama_csv/combined_logs.csv`

### Running Scripts Sequentially

Pull logs and convert in one command:

```bash
uv run python log-pull-per-second.py && uv run python xml_to_csv_converter.py
```

## Output Structure

### XML Files

```
panorama_logs/
├── logs_20251106_180000.xml
├── logs_20251106_180001.xml
├── logs_20251106_180002.xml
└── revisit_manually.md (if any queries hit limit)
```

### CSV Files

```
panorama_csv/
├── logs_20251106_180000.csv
├── logs_20251106_180001.csv
└── logs_20251106_180002.csv
```

### CSV Column Headers

Full Panorama traffic log schema with 118 columns including:
- Domain, Receive Time, Serial #
- Source/Destination addresses and ports
- NAT translations
- Application, User, Zone information
- Bytes, Packets, Session details
- Device information (OS, vendor, model)
- SD-WAN fields
- And more...

## Troubleshooting

### Error: "Please configure your API key"

**Solution:** Edit `.env` and set `PANORAMA_API_KEY`

### Error: "XML input directory not found"

**Solution:** Run `log-pull-per-second.py` first to create XML files

### Warning: "Query hit 5000 log limit"

**Meaning:** More logs exist for that second than retrieved

**Solution:** Check `revisit_manually.md` for affected queries. Manually refine with additional filters.

### SSL Certificate Warnings

Script disables SSL warnings by default. To enable:

Remove this line from scripts:
```python
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

### No Logs Found

**Check:**
1. Time range has actual traffic
2. API key has proper permissions
3. Panorama is reachable
4. Debug mode enabled to see API responses

## Performance Notes

- Each second = 1 API query
- 1 hour = 3600 queries
- Polling interval: 2 seconds (configurable)
- Processing ~300 files takes ~2-5 seconds

## File Locations

| Purpose | Location |
|---------|----------|
| Configuration | `.env` |
| Configuration Template | `.env.example` |
| Log Retrieval Script | `log-pull-per-second.py` |
| CSV Converter Script | `xml_to_csv_converter.py` |
| XML Output | `./panorama_logs/` |
| CSV Output | `./panorama_csv/` |
| Manual Review List | `./panorama_logs/revisit_manually.md` |

## Getting Panorama API Key

1. Login to Panorama web interface
2. Navigate to: **Panorama > Setup > Management**
3. Click **API Keys**
4. Generate new API key
5. Copy and paste into `.env`

## Log Types Supported

| Log Type | Description |
|----------|-------------|
| `traffic` | Traffic logs (default) |
| `threat` | Threat logs |
| `url` | URL filtering logs |
| `wildfire` | WildFire logs |
| `data` | Data filtering logs |
| `tunnel` | Tunnel logs |
| `auth` | Authentication logs |
| `userid` | User-ID logs |

## Dependencies

Managed automatically by `uv`:
- `requests>=2.31.0` - HTTP client
- `urllib3>=2.0.0` - HTTP library
- `python-dotenv>=1.0.0` - Environment variable loading

## License

See parent repository for license information.

## Support

For issues or questions, refer to the parent repository's issue tracker.
