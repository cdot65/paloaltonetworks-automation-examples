import requests
import json
import csv
import argparse
import logging
import time
import sys
import os
import tomllib

# Default configuration values
DEFAULT_CONFIG = {
    'api_key': '',
    'profile_id': '',
    'input_csv': 'prompts.csv',
    'output_csv': 'prompts_and_results.csv',
    'api': {
        'endpoint': 'https://service.api.aisecurity.paloaltonetworks.com/v1/scan/sync/request',
        'max_retries': 3,
        'retry_delay': 1
    },
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(levelname)s - %(message)s'
    }
}

def load_config(config_file):
    """Load configuration from TOML file."""
    config = DEFAULT_CONFIG.copy()
    
    if not os.path.exists(config_file):
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    
    with open(config_file, 'rb') as f:
        toml_config = tomllib.load(f)
        # Update with values from TOML file
        config.update(toml_config)
        # Handle nested dictionaries
        if 'api' in toml_config:
            config['api'].update(toml_config['api'])
        if 'logging' in toml_config:
            config['logging'].update(toml_config['logging'])
    
    return config

# Global variables to be set after config is loaded
config = None
url = None
headers = None
logger = None

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process prompts from CSV and scan with Palo Alto Networks AI Security Service')
    parser.add_argument('--config', type=str, default='config.toml', help='Path to TOML configuration file (default: config.toml)')
    return parser.parse_args()

def send_request_with_retry(payload, max_retries=None):
    """Send request with retry mechanism for client errors."""
    if max_retries is None:
        max_retries = config['api']['max_retries']
    
    for attempt in range(max_retries):
        try:
            # Start timing
            start_time = time.time()
            
            # Send request
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            
            # Calculate round trip time
            round_trip = round(time.time() - start_time, 3)
            
            # If successful or server error (5xx), return response
            if response.status_code < 400 or response.status_code >= 500:
                return response, round_trip
            
            # For client errors (4xx), retry if not the last attempt
            if attempt < max_retries - 1:
                logger.warning("Request failed with status %d. Retrying... (Attempt %d/%d)", response.status_code, attempt + 2, max_retries)
                time.sleep(config['api']['retry_delay'])
            else:
                return response, round_trip
                
        except Exception as e:
            logger.error("Request exception: %s", str(e))
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

def process_prompts(csv_file, profile_id, output_file):
    """Process prompts from CSV file and save results."""
    
    # Record start time
    process_start_time = time.time()
    logger.info("Processing started at %s", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(process_start_time)))
    
    # Check if input CSV exists
    if not os.path.exists(csv_file):
        logger.error("CSV file '%s' not found", csv_file)
        sys.exit(1)
    
    # Create output CSV with headers
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['prompt', 'action', 'category', 'scan_id', 'report_id', 'profile_name', 'round_trip', 'status_code'])
    
    # Read and process prompts
    with open(csv_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        
        # Skip header if present
        rows = list(reader)
        
        for index, row in enumerate(rows, start=1):
            # Skip empty rows
            if not row or not row[0].strip():
                continue
                
            prompt = row[0].strip()
            logger.info("Processing row %d: %s...", index, prompt[:50])
            
            # Prepare payload
            payload = {
                "tr_id": str(index),
                "ai_profile": {
                    "profile_id": profile_id
                },
                "contents": [
                    {
                        "prompt": prompt
                    }
                ]
            }
            
            try:
                # Send request with retry
                response, round_trip = send_request_with_retry(payload)
                
                # Extract values from response
                if response.status_code == 200:
                    data = response.json()
                    action = data.get('action', '')
                    category = data.get('category', '')
                    scan_id = data.get('scan_id', '')
                    report_id = data.get('report_id', '')
                    profile_name = data.get('profile_name', '')
                else:
                    # For error responses, use empty values
                    action = ''
                    category = ''
                    scan_id = ''
                    report_id = ''
                    profile_name = ''
                
                # Append results to CSV
                with open(output_file, 'a', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow([prompt, action, category, scan_id, report_id, profile_name, round_trip, response.status_code])
                
                logger.info("Row %d processed successfully (Status: %d)", index, response.status_code)
                
            except Exception as e:
                logger.error("Failed to process row %d: %s", index, str(e))
                # Write error entry to CSV
                with open(output_file, 'a', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow([prompt, '', '', '', '', '', 0, 'ERROR'])
    
    # Calculate and log total execution time
    process_end_time = time.time()
    total_duration = process_end_time - process_start_time
    
    logger.info("Processing complete! Results saved to '%s'", output_file)
    logger.info("Processing ended at %s", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(process_end_time)))
    logger.info("Total execution time: %.2f seconds (%.2f minutes)", total_duration, total_duration/60)

def main():
    """Main function."""
    global config, url, headers, logger
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Load configuration
    config = load_config(args.config)
    
    # Set up logging
    logging.basicConfig(
        level=getattr(logging, config['logging']['level']),
        format=config['logging']['format']
    )
    logger = logging.getLogger(__name__)
    
    # Validate required configuration
    if not config['api_key']:
        logger.error("API key not configured. Please set 'api_key' in config.toml file.")
        sys.exit(1)
    if not config['profile_id']:
        logger.error("Profile ID not configured. Please set 'profile_id' in config.toml file.")
        sys.exit(1)
    
    # Set up API configuration
    url = config['api']['endpoint']
    headers = {
        'x-pan-token': config['api_key'],
        'Content-Type': 'application/json'
    }
    
    logger.info("Starting prompt processing from '%s' with profile ID '%s'", config['input_csv'], config['profile_id'])
    logger.info("Configuration loaded from: %s", args.config)
    process_prompts(config['input_csv'], config['profile_id'], config['output_csv'])

if __name__ == "__main__":
    main()