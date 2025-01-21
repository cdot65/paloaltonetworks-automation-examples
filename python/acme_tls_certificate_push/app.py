import argparse
import os
import urllib3
import xml.etree.ElementTree as ET
import subprocess
import sys

"""
This script pushes a certificate file to Palo Alto Networks firewalls through their REST API.
It uses urllib3 to handle HTTP requests and ignores self-signed certificates without warnings.
The script accepts a list of devices as command-line arguments and deploys certificates to each.
"""

# Disable warnings for insecure requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Deploy certificates to Palo Alto Networks firewalls.")
    parser.add_argument("devices", help="Comma-separated list of device hostnames")
    parser.add_argument("--domain", default="cdot.io", help="Domain for the certificate (default: cdot.io)")
    parser.add_argument("--acme-path", default="/Users/cdot/.acme.sh/acme.sh", help="Path to acme.sh script")
    return parser.parse_args()

def deploy_certificate(device, domain, acme_path):
    """Deploy certificate to a single device."""
    print(f"Setting PANOS_HOST to {device}")

    # Create a copy of the current environment
    env = os.environ.copy()

    # Update PANOS_HOST in the environment, overwriting if it exists
    env['PANOS_HOST'] = device

    try:
        result = subprocess.run(
            [acme_path, "--deploy", "-d", domain, "--deploy-hook", "panos", "--insecure", "--debug"],
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Successfully deployed certificate to {device}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error deploying certificate to {device}: {e}")
        print(e.stderr)

def main():
    args = parse_arguments()
    devices = [device.strip() for device in args.devices.split(",")]

    for device in devices:
        deploy_certificate(device, args.domain, args.acme_path)

if __name__ == "__main__":
    main()

