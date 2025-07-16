#!/usr/bin/env python3
"""extract_device_groups.py

Utility script to read a Panorama running-config XML file and output a JSON
mapping for each device-group containing the security rule names in both the
*pre-rulebase* and *post-rulebase* sections.

The script:
1. Discovers all unique device-group names.
2. For each device group, collects rule names under:
   • `/pre-rulebase/security/rules`
   • `/post-rulebase/security/rules`
3. Prints a JSON object of the form:

    {
        "azure": {
            "pre": ["allow-apps", "deny-all"],
            "post": ["log-all"]
        },
        "magnolia-01": {
            "pre": [...],
            "post": [...]
        }
    }

Usage:
    python extract_device_groups.py /path/to/running-config.xml
If no path is provided, it defaults to a file called "running-config.xml" in the
current working directory.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path


def get_device_group_names(xml_path: str | Path) -> list[str]:
    """Return a list of unique device-group names in the order encountered."""
    xml_path = Path(xml_path).expanduser().resolve()
    if not xml_path.is_file():
        raise FileNotFoundError(f"XML file not found: {xml_path}")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Match every <device-group><entry name="..."> element anywhere in the XML
    names = [
        e.get("name") for e in root.findall(".//device-group/entry") if e.get("name")
    ]
    # Preserve order while removing duplicates
    unique_names = list(OrderedDict.fromkeys(names))
    return unique_names


def get_security_rules_by_group(
    xml_path: str | Path,
) -> dict[str, dict[str, list[str]]]:
    """Return mapping: device-group → {"pre": [...], "post": [...]} of rule names."""
    xml_path = Path(xml_path).expanduser().resolve()
    if not xml_path.is_file():
        raise FileNotFoundError(f"XML file not found: {xml_path}")

    tree = ET.parse(xml_path)
    root = tree.getroot()

    rules_map: dict[str, dict[str, list[str]]] = {}
    for dg_entry in root.findall(".//device-group/entry"):
        dg_name = dg_entry.get("name")
        if not dg_name:
            continue

        pre_rules = [
            e.get("name")
            for e in dg_entry.findall("./pre-rulebase/security/rules/entry")
            if e.get("name")
        ]
        post_rules = [
            e.get("name")
            for e in dg_entry.findall("./post-rulebase/security/rules/entry")
            if e.get("name")
        ]

        # Preserve order & uniqueness
        pre_rules = list(OrderedDict.fromkeys(pre_rules))
        post_rules = list(OrderedDict.fromkeys(post_rules))

        if dg_name in rules_map:
            rules_map[dg_name]["pre"] = list(
                OrderedDict.fromkeys(rules_map[dg_name]["pre"] + pre_rules)
            )
            rules_map[dg_name]["post"] = list(
                OrderedDict.fromkeys(rules_map[dg_name]["post"] + post_rules)
            )
        else:
            rules_map[dg_name] = {"pre": pre_rules, "post": post_rules}

    return rules_map


def write_rules_csv(rules: dict[str, dict[str, list[str]]], csv_path: Path) -> None:
    """Write rules mapping to CSV with columns: device_group, rulebase, rule_name."""
    csv_path = csv_path.expanduser().resolve()
    with csv_path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerow(["device_group", "rulebase", "rule_name"])
        for dg, sections in rules.items():
            for base, rule_list in sections.items():
                for rule in rule_list:
                    writer.writerow([dg, base, rule])


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Extract device-group names from a Panorama running-config XML file."
    )
    parser.add_argument(
        "xml_file",
        nargs="?",
        default="running-config.xml",
        help="Path to the running-config XML file (default: ./running-config.xml)",
    )
    parser.add_argument(
        "--csv",
        dest="csv_path",
        help="Optional output CSV file (default: <xml_file>.csv)",
    )
    args = parser.parse_args(argv)

    try:
        rules = get_security_rules_by_group(args.xml_file)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(rules, indent=2))

    # Write CSV
    csv_path = (
        Path(args.csv_path)
        if args.csv_path
        else Path(args.xml_file).with_suffix(".csv")
    )
    write_rules_csv(rules, csv_path)
    print(f"CSV written to {csv_path}")


if __name__ == "__main__":
    main()
