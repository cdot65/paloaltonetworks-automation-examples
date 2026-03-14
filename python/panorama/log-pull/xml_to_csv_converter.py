#!/usr/bin/env python3
"""
Panorama XML to CSV Converter
Converts XML log files retrieved from Panorama into CSV format.
"""

import csv
import logging
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

# Directory containing XML files
XML_INPUT_DIR = os.getenv("XML_INPUT_DIR", "./panorama_logs")

# Output configuration
CSV_OUTPUT_DIR = os.getenv("CSV_OUTPUT_DIR", "./panorama_csv")
CREATE_INDIVIDUAL_CSV = os.getenv("CREATE_INDIVIDUAL_CSV", "true").lower() in ("true", "1", "yes")

# Debug Configuration
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# CSV Column Headers (in order)
CSV_HEADERS = [
    'Domain',
    'Receive Time',
    'Serial #',
    'Type',
    'Threat/Content Type',
    'Config Version',
    'Generate Time',
    'Source address',
    'Destination address',
    'NAT Source IP',
    'NAT Destination IP',
    'Rule',
    'Source User',
    'Destination User',
    'Application',
    'Virtual System',
    'Source Zone',
    'Destination Zone',
    'Inbound Interface',
    'Outbound Interface',
    'Log Action',
    'Time Logged',
    'Session ID',
    'Repeat Count',
    'Source Port',
    'Destination Port',
    'NAT Source Port',
    'NAT Destination Port',
    'Flags',
    'IP Protocol',
    'Action',
    'Bytes',
    'Bytes Sent',
    'Bytes Received',
    'Packets',
    'Start Time',
    'Elapsed Time (sec)',
    'Category',
    '',  # Empty column
    'Sequence Number',
    'Action Flags',
    'Source Country',
    'Destination Country',
    '',  # Empty column
    'Packets Sent',
    'Packets Received',
    'Session End Reason',
    'DG Hierarchy Level 1',
    'DG Hierarchy Level 2',
    'DG Hierarchy Level 3',
    'DG Hierarchy Level 4',
    'Virtual System Name',
    'Device Name',
    'Action Source',
    'Source VM UUID',
    'Destination VM UUID',
    'Tunnel ID/IMSI',
    'Monitor Tag/IMEI',
    'Parent Session ID',
    'Parent Session Start Time',
    'Tunnel',
    'SCTP Association ID',
    'SCTP Chunks',
    'SCTP Chunks Sent',
    'SCTP Chunks Received',
    'UUID for rule',
    'HTTP/2 Connection',
    'link_change_count',
    'policy_id',
    'link_switches',
    'sdwan_cluster',
    'sdwan_device_type',
    'sdwan_cluster_type',
    'sdwan_site',
    'dynusergroup_name',
    'XFF address',
    'Source Device Category',
    'Source Device Profile',
    'Source Device Model',
    'Source Device Vendor',
    'Source Device OS Family',
    'Source Device OS Version',
    'Source Hostname',
    'Source Mac Address',
    'Destination Device Category',
    'Destination Device Profile',
    'Destination Device Model',
    'Destination Device Vendor',
    'Destination Device OS Family',
    'Destination Device OS Version',
    'Destination Hostname',
    'Destination Mac Address',
    'Container ID',
    'POD Namespace',
    'POD Name',
    'Source External Dynamic List',
    'Destination External Dynamic List',
    'Host ID',
    'Serial Number',
    'Source Dynamic Address Group',
    'Destination Dynamic Address Group',
    'session_owner',
    'High Res Timestamp',
    'nssai_sst',
    'nssai_sd',
    'Subcategory of app',
    'Category of app',
    'Technology of app',
    'Risk of app',
    'Characteristic of app',
    'Container of app',
    'Tunneled app',
    'SaaS of app',
    'Sanctioned State of app',
    'offloaded',
    'flow_type',
    'cluster_name'
]

# Mapping from XML element names to CSV columns
# XML uses underscores, CSV uses various formats
XML_TO_CSV_MAPPING = {
    'domain': 'Domain',
    'receive_time': 'Receive Time',
    'serial': 'Serial #',
    'type': 'Type',
    'subtype': 'Threat/Content Type',
    'config_ver': 'Config Version',
    'time_generated': 'Generate Time',
    'src': 'Source address',
    'dst': 'Destination address',
    'natsrc': 'NAT Source IP',
    'natdst': 'NAT Destination IP',
    'rule': 'Rule',
    'srcuser': 'Source User',
    'dstuser': 'Destination User',
    'app': 'Application',
    'vsys': 'Virtual System',
    'from': 'Source Zone',
    'to': 'Destination Zone',
    'inbound_if': 'Inbound Interface',
    'outbound_if': 'Outbound Interface',
    'logset': 'Log Action',
    'time_received': 'Time Logged',
    'sessionid': 'Session ID',
    'repeatcnt': 'Repeat Count',
    'sport': 'Source Port',
    'dport': 'Destination Port',
    'natsport': 'NAT Source Port',
    'natdport': 'NAT Destination Port',
    'flags': 'Flags',
    'proto': 'IP Protocol',
    'action': 'Action',
    'bytes': 'Bytes',
    'bytes_sent': 'Bytes Sent',
    'bytes_received': 'Bytes Received',
    'packets': 'Packets',
    'start': 'Start Time',
    'elapsed': 'Elapsed Time (sec)',
    'category': 'Category',
    'seqno': 'Sequence Number',
    'actionflags': 'Action Flags',
    'srcloc': 'Source Country',
    'dstloc': 'Destination Country',
    'pkts_sent': 'Packets Sent',
    'pkts_received': 'Packets Received',
    'session_end_reason': 'Session End Reason',
    'dg_hier_level_1': 'DG Hierarchy Level 1',
    'dg_hier_level_2': 'DG Hierarchy Level 2',
    'dg_hier_level_3': 'DG Hierarchy Level 3',
    'dg_hier_level_4': 'DG Hierarchy Level 4',
    'vsys_name': 'Virtual System Name',
    'device_name': 'Device Name',
    'action_source': 'Action Source',
    'src_uuid': 'Source VM UUID',
    'dst_uuid': 'Destination VM UUID',
    'tunnelid_imsi': 'Tunnel ID/IMSI',
    'monitortag_imei': 'Monitor Tag/IMEI',
    'parent_session_id': 'Parent Session ID',
    'parent_start_time': 'Parent Session Start Time',
    'tunnel': 'Tunnel',
    'assoc_id': 'SCTP Association ID',
    'chunks': 'SCTP Chunks',
    'chunks_sent': 'SCTP Chunks Sent',
    'chunks_received': 'SCTP Chunks Received',
    'rule_uuid': 'UUID for rule',
    'http2_connection': 'HTTP/2 Connection',
    'link_change_count': 'link_change_count',
    'policy_id': 'policy_id',
    'link_switches': 'link_switches',
    'sdwan_cluster': 'sdwan_cluster',
    'sdwan_device_type': 'sdwan_device_type',
    'sdwan_cluster_type': 'sdwan_cluster_type',
    'sdwan_site': 'sdwan_site',
    'dynusergroup_name': 'dynusergroup_name',
    'xff': 'XFF address',
    'src_category': 'Source Device Category',
    'src_profile': 'Source Device Profile',
    'src_model': 'Source Device Model',
    'src_vendor': 'Source Device Vendor',
    'src_osfamily': 'Source Device OS Family',
    'src_osversion': 'Source Device OS Version',
    'src_host': 'Source Hostname',
    'src_mac': 'Source Mac Address',
    'dst_category': 'Destination Device Category',
    'dst_profile': 'Destination Device Profile',
    'dst_model': 'Destination Device Model',
    'dst_vendor': 'Destination Device Vendor',
    'dst_osfamily': 'Destination Device OS Family',
    'dst_osversion': 'Destination Device OS Version',
    'dst_host': 'Destination Hostname',
    'dst_mac': 'Destination Mac Address',
    'container_id': 'Container ID',
    'pod_namespace': 'POD Namespace',
    'pod_name': 'POD Name',
    'src_edl': 'Source External Dynamic List',
    'dst_edl': 'Destination External Dynamic List',
    'hostid': 'Host ID',
    'serialnumber': 'Serial Number',
    'src_dag': 'Source Dynamic Address Group',
    'dst_dag': 'Destination Dynamic Address Group',
    'session_owner': 'session_owner',
    'high_res_timestamp': 'High Res Timestamp',
    'nssai_sst': 'nssai_sst',
    'nssai_sd': 'nssai_sd',
    'subcategory_of_app': 'Subcategory of app',
    'category_of_app': 'Category of app',
    'technology_of_app': 'Technology of app',
    'risk_of_app': 'Risk of app',
    'characteristic_of_app': 'Characteristic of app',
    'container_of_app': 'Container of app',
    'tunneled_app': 'Tunneled app',
    'saas_of_app': 'SaaS of app',
    'sanctioned_state_of_app': 'Sanctioned State of app',
    'offloaded': 'offloaded',
    'flow_type': 'flow_type',
    'cluster_name': 'cluster_name'
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def setup_output_directory():
    """Create output directory if it doesn't exist."""
    Path(CSV_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    logger.info(f"CSV output directory: {CSV_OUTPUT_DIR}")


def get_xml_files(directory):
    """
    Get all XML files from the specified directory.
    
    Args:
        directory: Path to directory containing XML files
        
    Returns:
        list: List of XML file paths
    """
    xml_files = []
    for file in Path(directory).glob("*.xml"):
        xml_files.append(file)
    
    xml_files.sort()  # Sort for consistent processing order
    return xml_files


def parse_xml_log(xml_file):
    """
    Parse XML file and extract log entries.
    
    Args:
        xml_file: Path to XML file
        
    Returns:
        list: List of dictionaries, each representing a log entry
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Find all log entries
        # Path: response/result/log/logs/entry
        entries = root.findall('.//result/log/logs/entry')

        if not entries:
            logger.warning(f"No log entries found in {xml_file}")
            return []

        log_entries = []

        for entry in entries:
            log_dict = {}

            # Extract all elements from the entry
            for element in entry:
                # Get the tag name and text content
                tag = element.tag
                text = element.text if element.text else ''
                log_dict[tag] = text

            log_entries.append(log_dict)

        logger.info(f"Parsed {len(log_entries)} entries from {xml_file.name}")
        return log_entries

    except ET.ParseError as e:
        logger.error(f"Failed to parse {xml_file}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error parsing {xml_file}: {e}")
        return []


def convert_log_to_csv_row(log_dict):
    """
    Convert a log dictionary to a CSV row based on column mapping.
    
    Args:
        log_dict: Dictionary containing log data from XML
        
    Returns:
        list: Ordered list of values matching CSV_HEADERS
    """
    row = []
    
    for header in CSV_HEADERS:
        if header == '':
            # Empty columns
            row.append('')
        else:
            # Find the corresponding XML field
            xml_field = None
            for xml_key, csv_key in XML_TO_CSV_MAPPING.items():
                if csv_key == header:
                    xml_field = xml_key
                    break
            
            if xml_field and xml_field in log_dict:
                row.append(log_dict[xml_field])
            else:
                row.append('')
    
    return row


def write_csv(csv_file, log_entries, mode='w'):
    """
    Write log entries to CSV file.
    
    Args:
        csv_file: Path to output CSV file
        log_entries: List of log dictionaries
        mode: File mode ('w' for write, 'a' for append)
    """
    try:
        write_header = mode == 'w' or not os.path.exists(csv_file)
        
        with open(csv_file, mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header if needed
            if write_header:
                writer.writerow(CSV_HEADERS)
            
            # Write data rows
            for log_entry in log_entries:
                row = convert_log_to_csv_row(log_entry)
                writer.writerow(row)
        
        return True

    except IOError as e:
        logger.error(f"Failed to write CSV {csv_file}: {e}")
        return False


def process_xml_to_csv(xml_files, individual=True):
    """
    Process XML files and convert to CSV.

    Args:
        xml_files: List of XML file paths
        individual: If True, create individual CSVs; if False, create one combined CSV
    """
    total_logs = 0
    total_files = 0

    if individual:
        # Individual CSV mode (default)
        logger.info(f"Creating individual CSV file for each XML file")

        for idx, xml_file in enumerate(xml_files, 1):
            logger.info(f"[{idx}/{len(xml_files)}] Processing: {xml_file.name}")

            # Parse XML
            log_entries = parse_xml_log(xml_file)

            if log_entries:
                # Create individual CSV with same base name
                csv_filename = xml_file.stem + '.csv'
                csv_path = os.path.join(CSV_OUTPUT_DIR, csv_filename)

                if write_csv(csv_path, log_entries):
                    total_logs += len(log_entries)
                    total_files += 1
                    logger.info(f"Created: {csv_path}")

        logger.info(f"Total CSV files created: {total_files}")
        logger.info(f"Total log entries processed: {total_logs}")

    else:
        # Combined CSV mode
        combined_csv_path = os.path.join(CSV_OUTPUT_DIR, "combined_logs.csv")
        logger.info(f"Creating combined CSV: {combined_csv_path}")

        # Remove existing file if it exists
        if os.path.exists(combined_csv_path):
            os.remove(combined_csv_path)

        for idx, xml_file in enumerate(xml_files, 1):
            logger.info(f"[{idx}/{len(xml_files)}] Processing: {xml_file.name}")

            # Parse XML
            log_entries = parse_xml_log(xml_file)

            if log_entries:
                # Append to combined CSV
                mode = 'w' if idx == 1 else 'a'
                if write_csv(combined_csv_path, log_entries, mode=mode):
                    total_logs += len(log_entries)

        logger.info(f"Combined CSV created: {combined_csv_path}")
        logger.info(f"Total log entries: {total_logs}")


# ============================================================================
# MAIN PROCESSING
# ============================================================================

def main():
    """Main processing function."""
    logger.info("=" * 80)
    logger.info("Panorama XML to CSV Converter")
    logger.info("=" * 80)

    # Setup
    setup_output_directory()

    # Check if input directory exists
    if not os.path.exists(XML_INPUT_DIR):
        logger.error(f"XML input directory not found: {XML_INPUT_DIR}")
        sys.exit(1)

    # Get XML files
    xml_files = get_xml_files(XML_INPUT_DIR)

    if not xml_files:
        logger.error(f"No XML files found in {XML_INPUT_DIR}")
        sys.exit(1)

    logger.info(f"Found {len(xml_files)} XML files to process")
    logger.info(f"Debug mode: {'enabled' if DEBUG else 'disabled'}")
    logger.info(f"Mode: {'Individual CSV files' if CREATE_INDIVIDUAL_CSV else 'Combined CSV file'}")
    logger.info("=" * 80)

    # Process files
    process_xml_to_csv(xml_files, individual=CREATE_INDIVIDUAL_CSV)

    logger.info("\n" + "=" * 80)
    logger.info("CONVERSION COMPLETE")
    logger.info("=" * 80)


if __name__ == "__main__":
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
