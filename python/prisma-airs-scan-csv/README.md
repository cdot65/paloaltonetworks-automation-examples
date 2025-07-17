# AI Security Testing Project

This project tests AI model responses to potentially harmful prompts using the Palo Alto Networks AI Security Service API.

## Installation

1. Install required dependencies from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the application:
   - Copy or rename `config.toml.example` to `config.toml` (if provided)
   - Or edit the existing `config.toml` file
   - Update the following required settings:
     - `api_key` - Your Palo Alto Networks AI Security Service API key
     - `profile_id` - Your AI profile ID for scanning

## Configuration

The application uses a TOML configuration file (`config.toml`) to manage settings. This file includes:

- **API Settings**: API key, profile ID, endpoint URL
- **File Settings**: Input/output CSV filenames
- **API Options**: Retry settings, delays
- **Logging**: Log level and format

Example `config.toml`:
```toml
# API Settings
api_key = "your-api-key-here"
profile_id = "your-profile-id-here"

# File Settings
input_csv = "test-prompts.csv"
output_csv = "results.csv"

# Optional Settings
[api]
endpoint = "https://service.api.aisecurity.paloaltonetworks.com/v1/scan/sync/request"
max_retries = 3
retry_delay = 1

[logging]
level = "INFO"
```

## Usage

### Run API Security Scans

The main script is `scan.py` which reads prompts from a CSV file and tests them against the AI Security Service.

#### Basic Usage
```bash
# Run with default settings from config.toml
python scan.py
```

#### Advanced Usage
```bash
# Use a different configuration file
python scan.py --config myconfig.toml
```

**Note for beginners**: 
- The `python` command runs Python scripts
- `scan.py` is the name of our main script
- `--config` is an optional parameter that lets you specify a different configuration file

The script will:
1. Load all settings from your `config.toml` file
2. Read prompts from the input CSV file (one prompt per line)
3. Send each prompt to the AI Security Service API for scanning
4. Automatically retry failed requests (up to 3 times by default)
5. Save results to the output CSV file with these columns:
   - `prompt`: The original text that was tested
   - `action`: What the AI Security Service decided (allow/block)
   - `category`: The type of potential issue detected
   - `scan_id`: Unique identifier for this scan
   - `report_id`: Report identifier for reference
   - `profile_name`: Name of the security profile used
   - `round_trip`: How long the request took (in seconds)
   - `status_code`: HTTP status code (200 = success)

## Files

### Input Files
- `test-prompts.csv` - Your test prompts (one per line)
- `config.toml` - Configuration file with API settings

### Output Files
- `results.csv` - The scan results (created automatically)

### Scripts
- `scan.py` - Main script that processes prompts and runs security scans

## Troubleshooting for Beginners

1. **"Configuration file not found" error**: Make sure `config.toml` exists in the same folder as `scan.py`

2. **"API key not configured" error**: Open `config.toml` and add your API key

3. **"CSV file not found" error**: Create a file named `test-prompts.csv` with your test prompts (one per line)

4. **Python not found**: Make sure Python is installed. You can check by running:
   ```bash
   python --version
   ```