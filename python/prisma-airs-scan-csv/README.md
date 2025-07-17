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
output_csv = "prompts_and_results.csv"

# Optional Settings
[api]
endpoint = "https://service.api.aisecurity.paloaltonetworks.com/v1/scan/sync/request"
max_retries = 3
retry_delay = 1

[logging]
level = "INFO"
```

## Usage

### Convert CSV to JSON format
```bash
python convert.py
```

This will read `test-prompts.csv` and create `test-prompts.json` with properly formatted API payloads.

### Run API tests
```bash
# Use default config.toml
python sync.py

# Use custom configuration file
python sync.py --config myconfig.toml

# Override specific settings via command line
python sync.py --csv custom-input.csv --output custom-output.csv

# Override profile ID
python sync.py --profile-id PROFILE123
```

The script will:
- Load configuration from the TOML file
- Process prompts from the input CSV file
- Send each prompt to the AI Security Service API
- Save results to the output CSV file with columns: prompt, action, category, scan_id, report_id, profile_name, round_trip, status_code

## Files

- `test-prompts.csv` - Source file containing test prompts
- `test-prompts.json` - Converted JSON format for API submission
- `test-prompts-results.json` - API response results
- `testprompts_with_results.csv` - Combined prompts with their test results