from panos_upgrade_assurance.firewall_proxy import FirewallProxy
from panos_upgrade_assurance.check_firewall import CheckFirewall


def run_readiness_checks(
    hostname: str, username: str, password: str, checks_configuration: list
) -> dict:
    """
    Run a series of readiness checks on a firewall using the CheckFirewall class.

    This function initializes a FirewallProxy instance, creates a CheckFirewall instance,
    and executes the specified readiness checks.

    Args:
        hostname (str): The hostname of the firewall.
        username (str): The API username for authentication.
        password (str): The API password for authentication.
        checks_configuration (list): A list of checks to be performed.

    Returns:
        dict: A dictionary containing the results of the readiness checks.

    Mermaid Workflow:
        ```mermaid
        graph TD
            A[Initialize FirewallProxy] --> B[Create CheckFirewall instance]
            B --> C[Run readiness checks]
            C --> D[Return results]
        ```
    """
    # Initialize the FirewallProxy
    firewall = FirewallProxy(
        hostname=hostname,
        api_username=username,
        api_password=password,
    )

    # Create a CheckFirewall instance
    checks = CheckFirewall(firewall)

    # Run the readiness checks
    results = checks.run_readiness_checks(checks_configuration)

    return results


def print_check_results(results: dict) -> None:
    """
    Print the results of the readiness checks.

    Args:
        results (dict): A dictionary containing the results of the readiness checks.

    Returns:
        None
    """
    for check, result in results.items():
        print(f"{check}: {'Passed' if result['state'] else 'Failed'}")
        if not result["state"]:
            print(f"  Reason: {result['reason']}")


def run_readiness_checks_example():
    """
    Demonstrate how to run readiness checks and print the results.

    This function shows an example of how to use the run_readiness_checks function
    and print the results using print_check_results.

    The checks_configuration list specifies the checks to be performed, which can include: - 'active_support': Check
    if active support is enabled. - 'candidate_config': Check if there is a candidate configuration. -
    'expired_licenses': Check for expired licenses. - 'jobs': Check for any running jobs. - 'ntp_sync': Check if NTP
    is synchronized. - 'panorama': Check if Panorama is connected. - {'content_version': {'version': '8634-7678'}}:
    Check if the content version matches the specified version. - {'free_disk_space': {'image_version':
    '10.1.6-h6'}}: Check if there is enough free disk space for the specified image version.

    Mermaid Workflow:
        ```mermaid
        graph TD
            A[Define checks configuration] --> B[Run readiness checks]
            B --> C[Print check results]
        ```
    """
    # Define the checks to run
    checks_configuration = [
        "active_support",
        "candidate_config",
        "expired_licenses",
        "jobs",
        "ntp_sync",
        "panorama",
        {"content_version": {"version": "8634-7678"}},
        {"free_disk_space": {"image_version": "10.1.6-h6"}},
    ]

    # Run the readiness checks
    results = run_readiness_checks(
        hostname="austin-fw1.cdot.io",
        username="officehours",
        password="paloalto123",
        checks_configuration=checks_configuration,
    )

    # Print the results
    print_check_results(results)


if __name__ == "__main__":
    run_readiness_checks_example()
