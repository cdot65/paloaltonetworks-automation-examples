from panos_upgrade_assurance.firewall_proxy import FirewallProxy
from panos_upgrade_assurance.check_firewall import CheckFirewall
from panos_upgrade_assurance.snapshot_compare import SnapshotCompare


def take_and_compare_snapshots(
    hostname: str,
    username: str,
    password: str,
    config_snapshots: list,
    config_comparison: list,
) -> dict:
    """
    Take pre- and post-upgrade snapshots of a firewall and compare them.

    This function initializes a FirewallProxy, takes pre- and post-upgrade snapshots,
    and compares them using the provided configuration.

    Args:
        hostname (str): The hostname of the firewall.
        username (str): The API username for authentication.
        password (str): The API password for authentication.
        config_snapshots (list): A list of areas to snapshot.
        config_comparison (list): A list of configurations for snapshot comparison.

    Returns:
        dict: A dictionary containing the comparison snapshot_comparison_result.

    Mermaid Workflow:
        ```mermaid
        graph TD
            A[Start] --> B[Initialize FirewallProxy]
            B --> C[Create CheckFirewall instance]
            C --> D[Take pre-upgrade snapshot]
            D --> E[Perform upgrade (not shown)]
            E --> F[Take post-upgrade snapshot]
            F --> G[Compare snapshots]
            G --> H[Return snapshot_comparison_result]
        ```
    """
    # Initialize the FirewallProxy
    firewall = FirewallProxy(
        hostname=hostname, api_username=username, api_password=password
    )

    # Create a CheckFirewall instance
    checks = CheckFirewall(firewall)

    # Take pre-upgrade snapshot
    print("Taking pre-upgrade snapshot...")
    pre_upgrade_snapshot = checks.run_snapshots(config_snapshots)

    # Perform upgrade here (not shown in this example)
    # ...

    # Take post-upgrade snapshot
    print("Taking post-upgrade snapshot...")
    post_upgrade_snapshot = checks.run_snapshots(config_snapshots)

    # Compare snapshots
    compare = SnapshotCompare(pre_upgrade_snapshot, post_upgrade_snapshot)

    # Run comparison
    snapshot_comparison_result = compare.compare_snapshots(config_comparison)

    return snapshot_comparison_result


def print_changes(changes: dict, indent: str = "") -> None:
    """
    Recursively print the changes detected in the snapshot comparison.

    Args:
        changes (dict): The dictionary containing the changes.
        indent (str, optional): The indentation string for formatting. Defaults to "".

    Returns:
        None
    """
    if isinstance(changes, dict):
        for key, value in changes.items():
            if key in ["passed", "missing_keys", "added_keys"]:
                continue
            print(f"{indent}{key}:")
            print_changes(value, indent + "  ")
    elif isinstance(changes, list):
        for item in changes:
            print(f"{indent}- {item}")
    else:
        print(f"{indent}{changes}")


def print_results(snapshot_comparison_result: dict) -> None:
    """
    Print the results of the snapshot comparison in a formatted manner.

    Args:
        snapshot_comparison_result (dict): The dictionary containing the comparison results.

    Returns:
        None
    """
    for area, result in snapshot_comparison_result.items():
        print(f"\n{area.upper()} comparison:")
        if result.get("passed", True):
            print("  No significant changes detected.")
        else:
            print("  Changes detected:")
            if "missing" in result and not result["missing"].get("passed", True):
                print(f"    Missing entries: {result['missing']['missing_keys']}")
            if "added" in result and not result["added"].get("passed", True):
                print(f"    Added entries: {result['added']['added_keys']}")
            if "changed" in result and not result["changed"].get("passed", True):
                print("    Changed entries:")
                print_changes(result["changed"].get("changed_raw", {}), "      ")
            if "count_change_percentage" in result:
                print(
                    f"    Count change percentage: {result['count_change_percentage']['change_percentage']}%"
                )
                print(
                    f"    Count change threshold: {result['count_change_percentage']['change_threshold']}%"
                )


# Main execution
if __name__ == "__main__":
    # Define the snapshot areas
    snapshot_config = [
        "nics",
        "routes",
        "license",
        "arp_table",
        "content_version",
        "session_stats",
        "ip_sec_tunnels",
    ]

    # Define comparison configuration
    comparison_config = [
        {"routes": {"count_change_threshold": 10}},
        {"arp_table": {"properties": ["!ttl"]}},
        "content_version",
        {"session_stats": {"thresholds": [{"num-max": 10}, {"num-tcp": 10}]}},
    ]

    # Take snapshots and compare
    results = take_and_compare_snapshots(
        hostname="austin-fw1.cdot.io",
        username="this-is-just-a-placeholder",
        password="this-is-just-a-placeholder",
        config_snapshots=snapshot_config,
        config_comparison=comparison_config,
    )

    # Print snapshot_comparison_result
    print_results(results)
