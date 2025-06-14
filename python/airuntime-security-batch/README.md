# AI Runtime Security Batch Scanner

A Python command-line tool for bulk scanning AI prompts and responses using Palo Alto Networks AI Runtime Security (AIRS) API. This tool enables security teams and developers to efficiently scan large volumes of AI interactions for potential threats and compliance issues.

## Overview

This tool processes batches of prompts and responses from CSV, JSON, or YAML files and submits them to the AIRS API for security scanning. It's designed for scenarios where you need to:

- Audit historical AI conversations for security threats
- Validate large datasets of AI interactions before deployment
- Perform compliance checks on AI-generated content at scale
- Test AI security profiles with diverse prompt scenarios

## Features

- **Multi-format Input Support**: Process prompts from CSV, JSON, or YAML files
- **Batch Processing**: Efficiently handles large volumes of data with configurable batch sizes
- **Asynchronous Operations**: Concurrent batch submissions for optimal performance
- **Flexible Configuration**: Supports environment variables and command-line arguments
- **Rich Logging**: Detailed progress tracking with configurable log levels
- **Error Handling**: Robust error management with detailed error reporting

## Requirements

- Python 3.8 or higher
- Palo Alto Networks AI Runtime Security API access
- Valid API key and AI profile configuration

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd airuntime-security-batch
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and add your AIRS credentials:

```bash
PANW_AI_SEC_API_KEY=your_api_key_here
PANW_AI_PROFILE_ID=your_profile_id_here
# Or use profile name instead:
# PANW_AI_PROFILE_NAME=your_profile_name_here

# Optional: Custom API endpoint (defaults to US endpoint)
# PANW_AI_SEC_API_ENDPOINT=https://service.api.aisecurity.paloaltonetworks.com
```

See `.env.example` for detailed configuration options and examples.

### Command-Line Options

```bash
python main.py --help

Options:
  --file FILE           Path to input file (CSV, JSON, or YAML) [required]
  --output OUTPUT       Save raw JSON batch responses to file
  --profile-name NAME   AI Profile name (overrides environment variable)
  --profile-id ID       AI Profile ID (overrides environment variable)
  --endpoint URL        Custom API endpoint
  --batch-size SIZE     Number of items per batch (default: 100)
  --log-level LEVEL     Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  --debug               Enable debug logging (shortcut for --log-level DEBUG)
```

## Input File Formats

### CSV Format

```csv
prompt,response
"What is the capital of France?","The capital of France is London."
"How do I make a cake?","To make a cake, first preheat your oven..."
```

### JSON Format

```json
[
  {
    "prompt": "What is the capital of France?",
    "response": "The capital of France is London."
  },
  {
    "prompt": "How do I make a cake?",
    "response": "To make a cake, first preheat your oven..."
  }
]
```

### YAML Format

```yaml
- prompt: "What is the capital of France?"
  response: "The capital of France is London."
- prompt: "How do I make a cake?"
  response: "To make a cake, first preheat your oven..."
```

## Usage Examples

### Basic Usage

```bash
python main.py --file prompts.csv
```

Example output:

```
2025-06-14 17:57:09,814 | INFO     | airs-batch-scan | Loading input file: prompts.csv
2025-06-14 17:57:09,814 | INFO     | airs-batch-scan | Submitting 1 batch(es)…
[Batch 1]  received=2025-06-14 22:57:10.067533+00:00  scan_id=f81c2ec8-29bd-4e58-9860-792cc6c340c5  report_id=Rf81c2ec8-29bd-4e58-9860-792cc6c340c5
```

### With Debug Logging

```bash
python main.py --file prompts.json --debug
```

Example output:

```
2025-06-14 17:57:15,215 | DEBUG    | airs-batch-scan | SDK initialised
2025-06-14 17:57:15,215 | DEBUG    | airs-batch-scan | Using AI profile: 946bf766-1533-4840-89c1-3cd7b5fd23c7
2025-06-14 17:57:15,215 | INFO     | airs-batch-scan | Loading input file: prompts.json
2025-06-14 17:57:15,215 | DEBUG    | airs-batch-scan | Loaded 2 row(s) from prompts.json
2025-06-14 17:57:15,215 | DEBUG    | airs-batch-scan | Constructed 2 AsyncScanObject(s)
2025-06-14 17:57:15,215 | INFO     | airs-batch-scan | Submitting 1 batch(es)…
2025-06-14 17:57:15,215 | DEBUG    | airs-batch-scan |  Batch 1: 2 object(s)
[Batch 1]  received=2025-06-14 22:57:15.432884+00:00  scan_id=25dd80e3-e6ec-4a61-a794-7e1d7ca72585  report_id=R25dd80e3-e6ec-4a61-a794-7e1d7ca72585
```

### Save Results to File

```bash
python main.py --file prompts.yaml --output results.json
```

Example output:

```
2025-06-14 17:57:44,065 | INFO     | airs-batch-scan | Loading input file: prompts.csv
2025-06-14 17:57:44,065 | INFO     | airs-batch-scan | Submitting 1 batch(es)…
[Batch 1]  received=2025-06-14 22:57:44.219916+00:00  scan_id=3de2d90a-e5cd-46ca-b291-5e7060194e48  report_id=R3de2d90a-e5cd-46ca-b291-5e7060194e48
2025-06-14 17:57:44,306 | INFO     | airs-batch-scan | Raw batch responses written to results.json
```

The saved `results.json` file contains:

```json
[
  {
    "received": "2025-06-14T22:57:44.219916+00:00",
    "scan_id": "3de2d90a-e5cd-46ca-b291-5e7060194e48",
    "report_id": "R3de2d90a-e5cd-46ca-b291-5e7060194e48"
  }
]
```

### Override Profile Configuration

```bash
python main.py --file prompts.csv --profile-name "Production-Security-Profile"
```

### Process Multiple Batches

For large files, the tool automatically splits them into batches based on the configured batch size:

```bash
python main.py --file large_dataset.csv
```

Example output:

```
2025-06-14 18:00:00,000 | INFO     | airs-batch-scan | Loading input file: large_dataset.csv
2025-06-14 18:00:00,000 | INFO     | airs-batch-scan | Submitting 3 batch(es)…
[Batch 1]  received=2025-06-14 23:00:00.123456+00:00  scan_id=aaaaaaaa-0000-4e0d-a2a6-215a0d5c56d9  report_id=Raaaaaaaa-0000-4e0d-a2a6-215a0d5c56d9
[Batch 2]  received=2025-06-14 23:00:00.234567+00:00  scan_id=bbbbbbbb-0000-5f1e-b3b7-326b1e6d67ea  report_id=Rbbbbbbbb-0000-5f1e-b3b7-326b1e6d67ea
[Batch 3]  received=2025-06-14 23:00:00.345678+00:00  scan_id=cccccccc-0000-6g2f-c4c8-437c2f7d78fb  report_id=Rcccccccc-0000-6g2f-c4c8-437c2f7d78fb
```

## Output

The tool displays scan results in the console with:

- **received**: Timestamp when the batch was processed
- **scan_id**: Unique identifier for the scan operation
- **report_id**: Report identifier (scan_id prefixed with 'R') for retrieving detailed threat reports

When using `--output`, the complete batch responses are saved as JSON for further analysis.

## Error Handling

The tool includes comprehensive error handling for:

- Missing or invalid credentials
- Malformed input files
- API connection issues
- Rate limiting
- Invalid batch sizes

All errors are logged with detailed information to help with troubleshooting.

## Security Considerations

- API keys should never be committed to version control
- Use environment variables or secure credential management systems
- The `.env` file is included in `.gitignore` by default
- Review scan results carefully before taking automated actions

## Limitations

- Large files are automatically split into multiple batches
- API rate limits apply based on your subscription tier
- Memory usage scales with file size

## Contributing

Please see [TODO.md](TODO.md) for planned improvements and feature requests.

## License

This project is part of the Palo Alto Networks automation examples repository. See the repository's main LICENSE file for details.

## Support

For issues related to:

- This tool: Please open an issue in this repository
- AIRS API: Contact Palo Alto Networks support
- API Documentation: Visit [pan.dev/ai-runtime-security](https://pan.dev/ai-runtime-security/)

## Related Resources

- [AIRS Python SDK Documentation](https://pan.dev/ai-runtime-security/api/pythonsdk/)
- [AIRS API Reference](https://pan.dev/ai-runtime-security/api/)
- [Palo Alto Networks AI Runtime Security](https://docs.paloaltonetworks.com/ai-runtime-security)
