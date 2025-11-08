#!/usr/bin/env python3
"""
Panorama Log Retrieval Script
Queries Panorama XML API for traffic logs second-by-second and saves results to local files.
Tracks queries that hit the 5000 log limit for manual review.
Enhanced with progress tracking to log when jobs have incomplete progress during polling.
"""

import logging
import os
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

# Panorama API Configuration
PANORAMA_HOSTNAME = os.getenv("PANORAMA_HOSTNAME", "magnolia1.cdot.io")
PANORAMA_URL = f"https://{PANORAMA_HOSTNAME}/api/"
API_KEY = os.getenv("PANORAMA_API_KEY", "your-api-key-here")

# Time Range Configuration
START_TIME = os.getenv("START_TIME", "2025/11/06 18:15:00")
END_TIME = os.getenv("END_TIME", "2025/11/06 18:20:00")

# Log Type Configuration
LOG_TYPE = os.getenv("LOG_TYPE", "traffic")
MAX_LOGS = int(os.getenv("MAX_LOGS", "5000"))

# Output Configuration
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./panorama_logs")
REVISIT_FILE = os.getenv("REVISIT_FILE", "revisit_manually.md")

# Polling Configuration
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "2"))
MAX_POLL_ATTEMPTS = int(os.getenv("MAX_POLL_ATTEMPTS", "60"))

# Debug Configuration
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def setup_output_directory():
    """Create output directory if it doesn't exist."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {OUTPUT_DIR}")


def parse_datetime(dt_string):
    """Parse datetime string in Panorama format."""
    return datetime.strptime(dt_string, "%Y/%m/%d %H:%M:%S")


def format_datetime(dt):
    """Format datetime object for Panorama query."""
    return dt.strftime("%Y/%m/%d %H:%M:%S")


def submit_log_query(start_dt, end_dt):
    """
    Submit a log query to Panorama and return the job ID.

    Args:
        start_dt: datetime object for query start
        end_dt: datetime object for query end

    Returns:
        tuple: (job_id, query_string) or (None, None) on error
    """
    query = f"( receive_time geq '{format_datetime(start_dt)}' ) and ( receive_time leq '{format_datetime(end_dt)}' )"

    params = {"type": "log", "log-type": LOG_TYPE, "query": query, "nlogs": MAX_LOGS}

    headers = {"X-PAN-KEY": API_KEY}

    try:
        logger.debug(f"Submitting query: {query}")
        response = requests.get(
            PANORAMA_URL, params=params, headers=headers, verify=False
        )
        response.raise_for_status()

        # Parse XML response
        root = ET.fromstring(response.text)

        # Check response status
        status = root.get("status")
        if status != "success":
            logger.error(f"Query failed: {response.text}")
            return None, None

        # Extract job ID
        job_element = root.find(".//job")
        if job_element is not None:
            job_id = job_element.text
            logger.info(f"Query submitted. Job ID: {job_id}")
            return job_id, query
        else:
            logger.error(f"No job ID in response: {response.text}")
            return None, None

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None, None
    except ET.ParseError as e:
        logger.error(f"XML parsing failed: {e}")
        return None, None


def poll_job_status(job_id):
    """
    Poll for job completion and return the XML response.

    Args:
        job_id: The job ID to poll

    Returns:
        tuple: (xml_response_text, incomplete_progress_count) or (None, 0) on error
    """
    params = {"type": "log", "action": "get", "job-id": job_id}

    headers = {"X-PAN-KEY": API_KEY}

    incomplete_count = 0  # Track how many times we see progress < 100

    for attempt in range(MAX_POLL_ATTEMPTS):
        try:
            response = requests.get(
                PANORAMA_URL, params=params, headers=headers, verify=False
            )
            response.raise_for_status()

            # Parse XML to check status
            root = ET.fromstring(response.text)
            status = root.get("status")

            if status == "success":
                # Check if job is complete
                job_status = root.find(".//status")
                if job_status is not None and job_status.text == "FIN":
                    # Check progress attribute in logs element
                    logs_element = root.find(".//logs")
                    if logs_element is not None:
                        progress = logs_element.get("progress")
                        if progress and int(progress) == 100:
                            logger.info(
                                f"Job {job_id} completed successfully (100% progress)"
                            )
                            if incomplete_count > 0:
                                logger.info(
                                    f"Job {job_id} had {incomplete_count} poll(s) with progress < 100%"
                                )
                            return response.text, incomplete_count
                        else:
                            incomplete_count += 1
                            logger.info(
                                f"Job {job_id} at {progress}% progress (attempt {attempt + 1}/{MAX_POLL_ATTEMPTS}) - incomplete #{incomplete_count}"
                            )
                            time.sleep(POLL_INTERVAL)
                    else:
                        # No logs element yet, keep polling
                        logger.info(
                            f"Job {job_id} still processing (no logs yet)... (attempt {attempt + 1}/{MAX_POLL_ATTEMPTS})"
                        )
                        time.sleep(POLL_INTERVAL)
                else:
                    logger.info(
                        f"Job {job_id} still processing... (attempt {attempt + 1}/{MAX_POLL_ATTEMPTS})"
                    )
                    time.sleep(POLL_INTERVAL)
            else:
                logger.error(f"Job {job_id} failed: {response.text}")
                return None, 0

        except requests.exceptions.RequestException as e:
            logger.error(f"Polling request failed: {e}")
            time.sleep(POLL_INTERVAL)
        except ET.ParseError as e:
            logger.error(f"XML parsing failed during polling: {e}")
            return None, 0

    logger.error(f"Job {job_id} timed out after {MAX_POLL_ATTEMPTS} attempts")
    return None, 0


def check_log_count(xml_text):
    """
    Check if the logs element has count=5000.

    Args:
        xml_text: XML response text

    Returns:
        bool: True if count is 5000, False otherwise
    """
    try:
        root = ET.fromstring(xml_text)
        logs_element = root.find(".//result/log/logs")

        if logs_element is not None:
            count = logs_element.get("count")
            if count and int(count) == MAX_LOGS:
                return True
        return False
    except Exception as e:
        logger.warning(f"Could not check log count: {e}")
        return False


def save_xml_response(xml_text, timestamp):
    """
    Save XML response to a timestamped file.

    Args:
        xml_text: XML response text
        timestamp: datetime object for the query

    Returns:
        str: Path to saved file
    """
    filename = f"logs_{timestamp.strftime('%Y%m%d_%H%M%S')}.xml"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_text)
        logger.info(f"Saved to: {filepath}")
        return filepath
    except IOError as e:
        logger.error(f"Failed to save file {filepath}: {e}")
        return None


def append_to_revisit_file(query, timestamp):
    """
    Append a query to the revisit file.

    Args:
        query: The query string that hit the limit
        timestamp: datetime object for the query
    """
    revisit_path = os.path.join(OUTPUT_DIR, REVISIT_FILE)

    try:
        with open(revisit_path, "a", encoding="utf-8") as f:
            f.write(f"\n## {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Query:** `{query}`\n")
            f.write(f"**Reason:** Hit maximum log count ({MAX_LOGS})\n")
            f.write(
                "**Action Required:** Manual review and potential re-query with refined filters\n"
            )
            f.write("\n---\n")
        logger.warning(f"Query added to {REVISIT_FILE} - hit {MAX_LOGS} log limit")
    except IOError as e:
        logger.error(f"Failed to write to {revisit_path}: {e}")


# ============================================================================
# MAIN PROCESSING
# ============================================================================


def main():
    """Main processing loop."""
    logger.info("=" * 80)
    logger.info("Panorama Log Retrieval Script")
    logger.info("=" * 80)

    # Validate configuration
    if API_KEY == "your-api-key-here":
        logger.error("Please configure your API key in the .env file")
        sys.exit(1)

    # Setup
    setup_output_directory()

    # Parse time range
    try:
        start_dt = parse_datetime(START_TIME)
        end_dt = parse_datetime(END_TIME)
    except ValueError as e:
        logger.error(f"Invalid datetime format: {e}")
        sys.exit(1)

    logger.info(f"Time range: {START_TIME} to {END_TIME}")
    logger.info(f"Log type: {LOG_TYPE}")
    logger.info(f"Max logs per query: {MAX_LOGS}")
    logger.info(f"Debug mode: {'enabled' if DEBUG else 'disabled'}")
    logger.info("=" * 80)

    # Calculate total iterations
    total_seconds = int((end_dt - start_dt).total_seconds())
    logger.info(f"Total queries to process: {total_seconds}")

    # Counters
    successful = 0
    failed = 0
    revisit_count = 0
    total_incomplete_polls = 0  # Track total incomplete progress events

    # Iterate second by second
    current_dt = start_dt

    while current_dt < end_dt:
        next_dt = current_dt + timedelta(seconds=1)

        logger.info(
            f"[{successful + failed + 1}/{total_seconds}] Processing: {format_datetime(current_dt)}"
        )

        # Submit query
        job_id, query = submit_log_query(current_dt, next_dt)

        if job_id:
            # Poll for completion (now returns incomplete_count too)
            xml_response, incomplete_count = poll_job_status(job_id)
            total_incomplete_polls += incomplete_count

            if xml_response:
                # Save the response
                saved_path = save_xml_response(xml_response, current_dt)

                if saved_path:
                    successful += 1

                    # Check if we hit the log limit
                    if check_log_count(xml_response):
                        append_to_revisit_file(query, current_dt)
                        revisit_count += 1
                else:
                    failed += 1
            else:
                failed += 1
        else:
            failed += 1

        # Move to next second
        current_dt = next_dt

    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("PROCESSING COMPLETE")
    logger.info("=" * 80)
    logger.info(f"Total queries: {successful + failed}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Queries requiring manual review: {revisit_count}")
    logger.info(f"Total incomplete progress polls: {total_incomplete_polls}")

    if total_incomplete_polls > 0:
        logger.warning("=" * 80)
        logger.warning(f"✓ Retry logic was triggered {total_incomplete_polls} time(s)")
        logger.warning("Jobs had progress < 100% during polling but completed successfully")
        logger.warning("=" * 80)

    if revisit_count > 0:
        logger.warning(
            f"Check {REVISIT_FILE} for queries that hit the {MAX_LOGS} log limit"
        )

    logger.info("=" * 80)


if __name__ == "__main__":
    # Suppress SSL warnings if needed
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nScript interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\nUnexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
