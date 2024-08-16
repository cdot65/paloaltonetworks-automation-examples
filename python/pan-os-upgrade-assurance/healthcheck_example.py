from panos_upgrade_assurance.firewall_proxy import FirewallProxy
from panos_upgrade_assurance.check_firewall import CheckFirewall


def run_health_checks(
    hostname: str, username: str, password: str, health_checks: list
) -> dict:
    """
    Run health checks on a firewall using the CheckFirewall class.

    This function initializes a FirewallProxy instance, creates a CheckFirewall instance,
    and executes the specified health checks on the firewall.

    Args:
        hostname (str): The hostname of the firewall.
        username (str): The API username for authentication.
        password (str): The API password for authentication.
        health_checks (list): A list of health checks to run.

    Returns:
        dict: A dictionary containing the results of the health checks.

    Mermaid Workflow:
        ```mermaid
        graph TD
            A[Start] --> B[Initialize FirewallProxy]
            B --> C[Create CheckFirewall instance]
            C --> D[Run health checks]
            D --> E[Return results]
            E --> F[End]
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

    # Run health checks
    results = checks.run_health_checks(health_checks)

    return results


def print_health_check_results(results: dict) -> None:
    """
    Print the results of the health checks in a formatted manner.

    Args:
        results (dict): A dictionary containing the results of the health checks.

    Returns:
        None
    """
    for check, result in results.items():
        print(f"{check}: {'Passed' if result['state'] else 'Failed'}")
        if not result["state"]:
            print(f"  Reason: {result['reason']}")


def run_health_checks_example() -> None:
    """
    Run an example of health checks on a firewall and print the results.

    This function demonstrates how to use the run_health_checks function
    and print_health_check_results function to perform health checks on a firewall.

    Returns:
        None

    Mermaid Workflow:
        ```mermaid
        graph TD
            A[Start] --> B[Define firewall credentials]
            B --> C[Define health checks]
            C --> D[Run health checks]
            D --> E[Print results]
            E --> F[End]
        ```
    """
    # Define firewall credentials
    hostname = "austin-fw1.cdot.io"
    username = "this-is-just-a-placeholder"
    password = "this-is-just-a-placeholder"

    # Define health checks
    health_checks = [
        "device_root_certificate_issue",
    ]

    # Run health checks
    results = run_health_checks(hostname, username, password, health_checks)

    # Print results
    print_health_check_results(results)


if __name__ == "__main__":
    run_health_checks_example()
