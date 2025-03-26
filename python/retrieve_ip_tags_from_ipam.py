#!/usr/bin/env python3
"""
Script to retrieve IP addresses from IPAM API and register them with Panorama
as IP tags with the values of "test", "python", "ipam".
"""

import os
import sys
import argparse
import ipaddress
import requests
from typing import Dict, List, Any
from urllib.parse import urljoin

from dotenv import load_dotenv
from panos.panorama import Panorama
from panos.userid import UserId


def load_credentials() -> Dict[str, str]:
    """Load credentials from environment variables."""
    load_dotenv()
    
    # Panorama credentials
    panorama_baseurl = os.getenv("PANORAMA_BASEURL")
    panorama_apikey = os.getenv("PANORAMA_APIKEY")
    
    # IPAM API credentials
    ipam_baseurl = os.getenv("IPAM_BASEURL", "https://dev.pomegranate.cdot.io/api/v1/ipam")
    ipam_token = os.getenv("IPAM_TOKEN")
    
    if not panorama_baseurl or not panorama_apikey:
        raise ValueError("Missing required Panorama environment variables")
    
    if not ipam_token:
        print("Warning: IPAM_TOKEN not found in environment variables")
        print("Using unauthenticated requests to IPAM API")
    
    # Add information about the API config
    print(f"Using IPAM API at: {ipam_baseurl}")
    
    return {
        "panorama_baseurl": panorama_baseurl,
        "panorama_apikey": panorama_apikey,
        "ipam_baseurl": ipam_baseurl,
        "ipam_token": ipam_token
    }


def create_panorama_connection(credentials: Dict[str, str]) -> Panorama:
    """Create a connection to Panorama."""
    try:
        panorama = Panorama(
            hostname=credentials["panorama_baseurl"],
            api_key=credentials["panorama_apikey"]
        )
        # Test connection
        panorama.refresh_system_info()
        print(f"Successfully connected to Panorama: {credentials['panorama_baseurl']}")
        return panorama
    except Exception as e:
        print(f"Error connecting to Panorama: {e}")
        if "Failed to authenticate" in str(e):
            print("API key authentication failed. Check your PANORAMA_APIKEY")
        elif ("Unknown SSL protocol error" in str(e) or
              "Connection refused" in str(e)):
            print("Connection issue. Verify PANORAMA_BASEURL is correct")
        sys.exit(1)


def fetch_ip_addresses(
    credentials: Dict[str, str], 
    vrf_id: str = None, 
    debug: bool = False,
    endpoint: str = "ip-addresses"
) -> List[Dict[str, Any]]:
    """
    Fetch data from the IPAM API.
    
    Args:
        credentials: Dictionary containing API credentials
        vrf_id: Optional VRF ID to filter results by
        debug: Enable debug output
        endpoint: API endpoint to query (default: "ip-addresses", can also be "prefixes")
    
    Returns:
        List of dictionaries containing IP information
    """
    ipam_url = credentials["ipam_baseurl"]
    
    # Ensure endpoint doesn't have leading slash but does have proper format
    if endpoint.startswith('/'):
        endpoint = endpoint[1:]
    
    # Add VRF filter if specified
    if vrf_id:
        endpoint += f"?vrf_id={vrf_id}"
    
    # Ensure the URL has a trailing slash
    if not ipam_url.endswith('/'):
        ipam_url += '/'
    
    url = urljoin(ipam_url, endpoint)
    
    headers = {
        "Accept": "application/json"
    }
    
    if credentials.get("ipam_token"):
        headers["Authorization"] = f"Bearer {credentials['ipam_token']}"
    
    if debug:
        print(f"DEBUG: Requesting URL: {url}")
        print(f"DEBUG: Headers: {headers}")
    
    try:
        # Make the API request
        response = requests.get(url, headers=headers, verify=True)
        
        if debug:
            print(f"DEBUG: Response status code: {response.status_code}")
            print(f"DEBUG: Response headers: {response.headers}")
            print(f"DEBUG: Response content type: {response.headers.get('Content-Type', 'unknown')}")
            print(f"DEBUG: Response content preview: {response.text[:200]}...")
        
        # Check if response is successful
        response.raise_for_status()
        
        # Attempt to parse JSON - based on your curl examples, the API returns a JSON array directly
        try:
            data = response.json()
            
            if debug:
                print(f"DEBUG: Successfully parsed JSON response")
                print(f"DEBUG: Number of items in response: {len(data) if isinstance(data, list) else 'Not a list'}")
                print(f"DEBUG: Data type: {type(data)}")
                if isinstance(data, list) and len(data) > 0:
                    print(f"DEBUG: First item keys: {data[0].keys()}")
            
            # Handle the response format - from your curl example, it returns a JSON array directly
            if isinstance(data, list):
                return data
            # If it's a single object, wrap it in a list
            elif isinstance(data, dict):
                return [data]
            # Check if there's a results key
            elif isinstance(data, dict) and 'results' in data:
                return data['results']
            # Fallback
            else:
                print(f"WARNING: Unexpected response format from IPAM API: {type(data)}")
                return []
            
        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response content: {response.text[:200]}...")
            
            # Fallback to mock data if debug is enabled
            if debug:
                print("DEBUG: Using mock data for testing since API response failed")
                if endpoint == "prefixes":
                    return [
                        {"prefix": "10.0.0.0/8", "status": "active", "description": "Test Prefix 1"},
                        {"prefix": "192.168.0.0/16", "status": "active", "description": "Test Prefix 2"},
                        {"prefix": "172.16.0.0/12", "status": "active", "description": "Private Network"}
                    ]
                else:
                    return [
                        {"address": "10.0.0.1/32", "status": "active", "description": "Test IP 1"},
                        {"address": "10.0.0.2/32", "status": "active", "description": "Test IP 2"},
                        {"address": "192.168.1.1/24", "status": "active", "description": "Gateway"}
                    ]
            sys.exit(1)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from IPAM API endpoint '{endpoint}': {e}")
        if debug:
            print("DEBUG: Using mock data for testing since API connection failed")
            if endpoint == "prefixes":
                return [
                    {"prefix": "10.0.0.0/8", "status": "active", "description": "Test Prefix 1"},
                    {"prefix": "192.168.0.0/16", "status": "active", "description": "Test Prefix 2"},
                    {"prefix": "172.16.0.0/12", "status": "active", "description": "Private Network"}
                ]
            else:
                return [
                    {"address": "10.0.0.1/32", "status": "active", "description": "Test IP 1"},
                    {"address": "10.0.0.2/32", "status": "active", "description": "Test IP 2"},
                    {"address": "192.168.1.1/24", "status": "active", "description": "Gateway"}
                ]
        sys.exit(1)


def register_ip_tags(panorama: Panorama, ip_addresses: List[Dict[str, Any]], 
                    default_tags: List[str] = None, timeout: int = None, 
                    simulation: bool = False, debug: bool = False, 
                    use_payload_tags_only: bool = True) -> None:
    """
    Register IP addresses with Panorama as IP tags.
    
    Args:
        panorama: The Panorama connection object
        ip_addresses: List of IP address dictionaries from IPAM API
        default_tags: List of default tags to use if no tags in payload (only used if use_payload_tags_only=False)
        timeout: Optional timeout in seconds (None = persists until cleared)
        simulation: Whether to simulate the operation without making changes
        debug: Enable debug output
        use_payload_tags_only: If True, only use tags from the API payload
    """
    # Create a User-ID object if not in simulation mode
    userid = None
    if not simulation:
        userid = UserId(panorama)
    
    registered_count = 0
    skipped_count = 0
    no_tags_count = 0
    
    if debug:
        print(f"DEBUG: Processing {len(ip_addresses)} IP addresses")
        print(f"DEBUG: Using tags from payload only: {use_payload_tags_only}")
    
    for ip_data in ip_addresses:
        try:
            if debug:
                print(f"DEBUG: Processing IP data: {ip_data}")
                
            # Extract IP address from the IPAM data
            # Address format could be "10.1.1.1/24" or similar
            if 'address' not in ip_data:
                print(f"Skipping entry without address field: {ip_data}")
                skipped_count += 1
                continue
            
            # Get the full address including CIDR notation if present
            full_address = ip_data['address']
            
            # Detect if this is a network prefix or a single IP
            is_prefix = '/' in full_address
            
            # Get description or other metadata if available
            description = ip_data.get('description', 'No description')
            status = ip_data.get('status', 'unknown')
            
            # Extract tags from the IP data payload
            payload_tags = ip_data.get('tags', None)
            
            # Determine which tags to use
            tags_to_apply = []
            
            if payload_tags and isinstance(payload_tags, list):
                # Use tags from the payload
                tags_to_apply = payload_tags
                if debug:
                    print(f"DEBUG: Using {len(tags_to_apply)} tags from payload: {tags_to_apply}")
            elif payload_tags and isinstance(payload_tags, str):
                # Handle case where tags might be a comma-separated string
                tags_to_apply = [tag.strip() for tag in payload_tags.split(',')]
                if debug:
                    print(f"DEBUG: Parsed {len(tags_to_apply)} tags from string: {tags_to_apply}")
            elif not use_payload_tags_only and default_tags:
                # Use default tags if allowed and available
                tags_to_apply = default_tags
                if debug:
                    print(f"DEBUG: Using {len(tags_to_apply)} default tags: {tags_to_apply}")
            else:
                # No tags to apply
                if debug:
                    print(f"DEBUG: No tags found in payload for {full_address}, skipping tag registration")
                no_tags_count += 1
                continue
            
            if debug:
                print(f"DEBUG: Using address: {full_address}, Status: {status}, Description: {description}")
                print(f"DEBUG: Will apply {len(tags_to_apply)} tags: {tags_to_apply}")
            
            # Skip if no tags to apply
            if not tags_to_apply:
                if debug:
                    print(f"DEBUG: No tags to apply for {full_address}, skipping")
                no_tags_count += 1
                continue
            
            # Validate the IP address or network
            try:
                if is_prefix:
                    # Validate as a network
                    ipaddress.ip_network(full_address, strict=False)
                else:
                    # Validate as a single IP
                    ipaddress.ip_address(full_address)
            except ValueError:
                print(f"Skipping invalid IP address or network: {full_address}")
                skipped_count += 1
                continue
                
            # In simulation mode, just print what would happen
            if simulation:
                for tag in tags_to_apply:
                    print(f"SIMULATION: Would register {full_address} with tag '{tag}'")
                    if debug:
                        if is_prefix:
                            print(f"DEBUG: Network prefix detected, registering entire subnet")
                        print(f"DEBUG: IP details: Status={status}, Description={description}")
                registered_count += 1
                continue
                
            # Register each tag for the IP address
            for tag in tags_to_apply:
                try:
                    # Use the full address including CIDR notation if present
                    userid.register(full_address, tag, timeout=timeout)
                    print(f"Successfully registered {full_address} with tag '{tag}'")
                    if debug:
                        if is_prefix:
                            print(f"  - Network prefix detected, registered entire subnet")
                        if description:
                            print(f"  - Description: {description}")
                except Exception as e:
                    print(f"Error registering {full_address} with tag '{tag}': {e}")
                    
            registered_count += 1
            
        except Exception as e:
            print(f"Error processing IP address entry: {e}")
            if debug:
                import traceback
                traceback.print_exc()
            skipped_count += 1
    
    print(f"\nRegistration complete:")
    print(f"  - Successfully processed: {registered_count} IP addresses/networks")
    print(f"  - Skipped (invalid/missing data): {skipped_count} IP addresses/networks")
    print(f"  - Skipped (no tags): {no_tags_count} IP addresses/networks")


def main() -> None:
    """Main function to execute the script."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Retrieve IP addresses from IPAM and register them with Panorama as IP tags"
    )
    
    parser.add_argument(
        "--vrf",
        help="Filter IP addresses by VRF ID"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        help="Optional timeout in seconds (default: no timeout)"
    )
    
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Run in simulation mode (no actual changes)"
    )
    
    parser.add_argument(
        "--tags",
        default="test,python,ipam",
        help="Default tags to apply if not using payload-only mode"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output"
    )
    
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock IP data instead of fetching from API"
    )
    
    parser.add_argument(
        "--ip-only",
        action="store_true",
        help="Only retrieve IP addresses and display them without registering tags"
    )
    
    parser.add_argument(
        "--api-url",
        help="Override the IPAM API URL from environment variable"
    )
    
    parser.add_argument(
        "--use-default-tags",
        action="store_true",
        help="Use default tags from --tags for IPs without tags in payload"
    )
    
    parser.add_argument(
        "--payload-tags-only", 
        action="store_true",
        help="Only use tags from the API payload (default behavior)"
    )
    
    parser.add_argument(
        "--prefixes",
        action="store_true",
        help="Fetch and process prefixes from the API instead of IP addresses"
    )
    
    args = parser.parse_args()
    
    # Convert tags to a list
    default_tags = [tag.strip() for tag in args.tags.split(',')]
    
    # Determine tag source behavior
    use_payload_tags_only = True
    if args.use_default_tags:
        use_payload_tags_only = False
    
    try:
        print("Loading credentials...")
        credentials = load_credentials()
        
        # Override API URL if provided
        if args.api_url:
            credentials["ipam_baseurl"] = args.api_url
            print(f"Overriding IPAM API URL to: {args.api_url}")
        
        if args.debug:
            print("DEBUG MODE ENABLED")
        
        if args.simulate:
            print("Running in SIMULATION mode - no changes will be made to Panorama")
            panorama = None
        else:
            print("Connecting to Panorama...")
            panorama = create_panorama_connection(credentials)
        
        # Use mock data if requested
        if args.mock:
            print("Using mock IP address data with tags...")
            ip_addresses = [
                {"address": "10.0.0.1/32", "status": "active", "description": "Test IP 1", "tags": ["web", "frontend"]},
                {"address": "10.0.0.2/32", "status": "active", "description": "Test IP 2", "tags": ["db", "backend"]},
                {"address": "192.168.1.1/24", "status": "active", "description": "Gateway", "tags": ["infrastructure"]},
                {"address": "192.168.1.10/24", "status": "active", "description": "Server", "tags": ["app", "backend"]},
                {"address": "172.16.0.1/24", "status": "active", "description": "Test IP 3", "tags": None},
                {"address": "192.168.13.0/24", "status": "active", "description": "Network prefix example", "tags": ["network", "subnet"]}
            ]
            print(f"Using {len(ip_addresses)} mock IP addresses")
        else:
            # Choose which endpoint to use based on arguments
            if args.prefixes:
                print("Fetching prefixes from IPAM API...")
                endpoint = "prefixes"
                # Use the prefix field as the address field for consistent processing
                ip_addresses = fetch_ip_addresses(credentials, args.vrf, args.debug, endpoint=endpoint)
                
                # Convert the "prefix" field to "address" for consistent processing
                for ip_data in ip_addresses:
                    if 'prefix' in ip_data and 'address' not in ip_data:
                        ip_data['address'] = ip_data['prefix']
                
                print(f"Retrieved {len(ip_addresses)} prefixes")
            else:
                print("Fetching IP addresses from IPAM API...")
                ip_addresses = fetch_ip_addresses(credentials, args.vrf, args.debug)
                print(f"Retrieved {len(ip_addresses)} IP addresses")
        
        # Display IP addresses if requested
        if args.ip_only or args.debug:
            print("\nIP Addresses/Networks retrieved:")
            for i, ip_data in enumerate(ip_addresses[:20], 1):  # Limit to first 20 for display
                ip = ip_data.get('address', ip_data.get('prefix', 'Unknown'))
                desc = ip_data.get('description', '')
                status = ip_data.get('status', '')
                tags = ip_data.get('tags', None)
                
                # Check if it's a network prefix
                is_prefix = '/' in ip
                prefix_info = " [network prefix]" if is_prefix else ""
                
                tags_info = f" - Tags: {tags}" if tags else " - No tags"
                print(f"  {i}. {ip}{prefix_info} - Status: {status}" + (f" - {desc}" if desc else "") + tags_info)
            
            if len(ip_addresses) > 20:
                print(f"  ... and {len(ip_addresses) - 20} more")
                
            # Exit if only displaying IPs
            if args.ip_only:
                print("\nRetrieved IP addresses/networks only. Exiting without registering tags.")
                return
        
        # Tag usage message
        if use_payload_tags_only:
            print("\nUsing ONLY tags from the API payload. Addresses without tags will be skipped.")
        else:
            print(f"\nUsing tags from API payload. For addresses without tags, using default tags: {', '.join(default_tags)}")
        
        if args.simulate:
            register_ip_tags(
                panorama=None, 
                ip_addresses=ip_addresses, 
                default_tags=default_tags, 
                timeout=args.timeout, 
                simulation=True, 
                debug=args.debug,
                use_payload_tags_only=use_payload_tags_only
            )
        else:
            print("\nRegistering IP addresses/networks with Panorama...")
            register_ip_tags(
                panorama=panorama, 
                ip_addresses=ip_addresses, 
                default_tags=default_tags, 
                timeout=args.timeout, 
                debug=args.debug,
                use_payload_tags_only=use_payload_tags_only
            )
        
    except Exception as e:
        print(f"Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
