import requests
import json
import csv
import argparse
import logging
import time
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API endpoint
url = "https://service.api.aisecurity.paloaltonetworks.com/v1/scan/sync/request"

# Headers with authentication
headers = {
    'x-pan-token': 'YOUR-API-TOKEN-GOES-RIGHT-HERE!!!',
    'Content-Type': 'application/json'
}

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process prompts from CSV and scan with Prisma AIRS')
    parser.add_argument('--csv', type=str, default='prompts.csv', help='Path to input CSV file (default: prompts.csv)')
    parser.add_argument('--profile-id', type=str, required=True, help='Profile ID for AI profile')
    return parser.parse_args()

def send_request_with_retry(payload, max_retries=3):
    """Send request with retry mechanism for client errors."""
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
                logger.warning(f"Request failed with status {response.status_code}. Retrying... (Attempt {attempt + 2}/{max_retries})")
                time.sleep(1)  # Wait 1 second before retry
            else:
                return response, round_trip

        except Exception as e:
            logger.error(f"Request exception: {str(e)}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)

def process_prompts(csv_file, profile_id):
    """Process prompts from CSV file and save results."""
    output_file = 'prompts_and_results.csv'

    # Record start time
    process_start_time = time.time()
    logger.info(f"Processing started at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(process_start_time))}")

    # Check if input CSV exists
    if not os.path.exists(csv_file):
        logger.error(f"CSV file '{csv_file}' not found")
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
            logger.info(f"Processing row {index}: {prompt[:50]}...")

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

                logger.info(f"Row {index} processed successfully (Status: {response.status_code})")

            except Exception as e:
                logger.error(f"Failed to process row {index}: {str(e)}")
                # Write error entry to CSV
                with open(output_file, 'a', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow([prompt, '', '', '', '', '', 0, 'ERROR'])

    # Calculate and log total execution time
    process_end_time = time.time()
    total_duration = process_end_time - process_start_time

    logger.info(f"Processing complete! Results saved to '{output_file}'")
    logger.info(f"Processing ended at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(process_end_time))}")
    logger.info(f"Total execution time: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")

def main():
    """Main function."""
    args = parse_arguments()

    logger.info(f"Starting prompt processing from '{args.csv}' with profile ID '{args.profile_id}'")
    process_prompts(args.csv, args.profile_id)

if __name__ == "__main__":
    main()
