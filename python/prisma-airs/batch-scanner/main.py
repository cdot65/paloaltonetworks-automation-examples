#!/usr/bin/env python3
"""
airs_batch_scan.py – Bulk‑scan prompts with Palo Alto Networks
AI Runtime Security (AIRS) via the pan‑aisecurity Python SDK.

Refactored version with improved code quality:
• Direct Pydantic attribute access (no _field helper)
• Full type hints
• Constants for magic numbers
• Simplified batched function
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import logging
import os
import pathlib
import sys
from typing import Any, Dict, List, Optional, Tuple

import dotenv
import yaml  # PyYAML
import aisecurity
from tabulate import tabulate

from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
from aisecurity.generated_openapi_client import (
    AsyncScanObject,
    ScanRequest,
    ScanRequestContentsInner,
    ScanIdResult,
)
from aisecurity.scan.asyncio.scanner import Scanner

# --------------------------------------------------------------------------- #
#                               Constants                                     #
# --------------------------------------------------------------------------- #

# Polling configuration
DEFAULT_POLL_ATTEMPTS = 20
POLL_INTERVAL_SECONDS = 2

# Display configuration
TEXT_TRUNCATE_LENGTH = 80
DISPLAY_WIDTH = 120
DIVIDER = "=" * DISPLAY_WIDTH
SUBDIV = "-" * DISPLAY_WIDTH

# Batch configuration
DEFAULT_BATCH_SIZE = 1000

# Violation type mappings
PROMPT_VIOLATION_FIELDS = [
    "agent",
    "dlp",
    "injection",
    "toxic_content",
    "url_cats",
]
RESPONSE_VIOLATION_FIELDS = [
    "dlp",
    "toxic_content",
    "url_cats",
    "db_security",
    "ungrounded",
]

# Display names for violations
VIOLATION_DISPLAY_NAMES = {
    "toxic_content": "toxic",
    "url_cats": "url",
    "db_security": "db_sec",
}

# --------------------------------------------------------------------------- #
#                               logging setup                                 #
# --------------------------------------------------------------------------- #

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
logging.basicConfig(format=LOG_FORMAT, stream=sys.stdout)
log = logging.getLogger("airs-batch-scan")


def configure_logging(level_str: Optional[str], debug_flag: bool) -> None:
    """Configure logging levels for the application and dependencies."""
    level = logging.DEBUG if debug_flag else logging.getLevelName(level_str or "INFO")
    logging.getLogger().setLevel(level)
    # Bridge SDK & aiohttp logs
    logging.getLogger("aisecurity").setLevel(level)
    logging.getLogger("aiohttp.client").setLevel(level)


# --------------------------------------------------------------------------- #
#                             Utility functions                               #
# --------------------------------------------------------------------------- #


def batched(iterable, n: int):
    """
    Batch an iterable into chunks of size n.

    For Python 3.12+, uses the built-in itertools.batched.
    For earlier versions, provides a simple implementation.
    """
    import itertools

    # Try to use the built-in if available
    if hasattr(itertools, "batched"):
        yield from itertools.batched(iterable, n)
        return

    # Simple implementation for older Python versions
    iterator = iter(iterable)
    while True:
        batch = list(itertools.islice(iterator, n))
        if not batch:
            return
        yield batch


def load_input_file(path: pathlib.Path) -> List[Dict[str, Optional[str]]]:
    """
    Parse CSV, JSON, or YAML into a list of {'prompt': ..., 'response': ...}.
    """
    log.info("Loading input file: %s", path)
    ext = path.suffix.lower()
    if ext == ".csv":
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [
                {"prompt": r.get("prompt"), "response": r.get("response")}
                for r in reader
            ]
    elif ext in (".yml", ".yaml"):
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        rows = _normalise_yaml_json(data)
    elif ext == ".json":
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        rows = _normalise_yaml_json(data)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    log.debug("Loaded %d row(s) from %s", len(rows), path)
    return rows


def _normalise_yaml_json(data: Any) -> List[Dict[str, Optional[str]]]:
    """
    Normalise YAML/JSON structures to a list[dict(prompt, response)].
    """
    if isinstance(data, dict):
        data = list(data.values())
    normalised: List[Dict[str, Optional[str]]] = []
    for item in data:
        if isinstance(item, (list, tuple)):
            prompt, *rest = item
            normalised.append({"prompt": prompt, "response": rest[0] if rest else None})
        elif isinstance(item, dict):
            normalised.append(
                {
                    "prompt": item.get("prompt")
                    or item.get("input")
                    or item.get("question"),
                    "response": item.get("response")
                    or item.get("output")
                    or item.get("answer"),
                }
            )
        else:  # bare string
            normalised.append({"prompt": str(item), "response": None})
    return normalised


def build_scan_objects(
    scan_contents: List[Dict[str, Optional[str]]],
    ai_profile: AiProfile,
) -> Tuple[List[AsyncScanObject], Dict[int, Dict[str, Optional[str]]]]:
    """Build AsyncScanObject list and content mapping."""
    async_objects: List[AsyncScanObject] = []
    req_id = 0
    content_map = {}
    for sc in scan_contents:
        req_id += 1
        content_map[req_id] = sc
        async_objects.append(
            AsyncScanObject(
                req_id=req_id,
                scan_req=ScanRequest(
                    ai_profile=ai_profile,
                    contents=[
                        ScanRequestContentsInner(
                            prompt=sc["prompt"],
                            response=sc["response"],
                        )
                    ],
                ),
            )
        )
    log.debug("Constructed %d AsyncScanObject(s)", len(async_objects))
    return async_objects, content_map


async def run_batches(
    async_objects: List[AsyncScanObject],
    batch_size: int,
    endpoint_override: Optional[str] = None,
) -> List[Any]:
    """
    Submit batches concurrently and return list of AsyncScanResponse.
    """
    scanner = Scanner()
    if endpoint_override:
        scanner.api_endpoint = endpoint_override  # type: ignore[attr-defined]

    batches = list(batched(async_objects, batch_size))
    log.info("Submitting %d batch(es)…", len(batches))
    for i, b in enumerate(batches, 1):
        log.debug(" Batch %d: %d object(s)", i, len(b))

    coroutines = [scanner.async_scan(batch) for batch in batches]
    try:
        responses = await asyncio.gather(*coroutines)
    finally:
        await scanner.close()

    return responses


def pretty_print_batch_results(batch_results: List[Any]) -> None:
    """Print batch submission results."""
    for idx, res in enumerate(batch_results, start=1):
        print(
            f"[Batch {idx}]  received={res.received!s:<5}  "
            f"scan_id={res.scan_id}  report_id={res.report_id}"
        )


def get_violations(detected_obj: Any, violation_fields: List[str]) -> List[str]:
    """Extract violations from a detection object."""
    violations = []
    for field in violation_fields:
        if getattr(detected_obj, field, False):
            display_name = VIOLATION_DISPLAY_NAMES.get(field, field)
            violations.append(display_name)
    return violations


async def retrieve_and_display_results(
    scanner: Scanner,
    batch_results: List[Any],
    content_map: Dict[int, Dict[str, Optional[str]]],
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Retrieve scan results and display them in a tabular format.
    Returns a dictionary with detailed categorization of prompts and responses.
    """
    # Collect all scan IDs
    scan_ids = [res.scan_id for res in batch_results]

    log.info("Retrieving scan results for %d scan(s)...", len(scan_ids))

    # Query for scan results with polling to wait for all results
    total_expected = len(content_map)
    scan_results: List[ScanIdResult] = []

    for attempt in range(DEFAULT_POLL_ATTEMPTS):
        scan_results = await scanner.query_by_scan_ids(scan_ids=scan_ids)
        log.debug(
            "Polling attempt %d: Retrieved %d/%d scan results",
            attempt + 1,
            len(scan_results),
            total_expected,
        )

        if len(scan_results) >= total_expected:
            log.info("All %d results received", len(scan_results))
            break

        if attempt < DEFAULT_POLL_ATTEMPTS - 1:
            await asyncio.sleep(POLL_INTERVAL_SECONDS)

    if len(scan_results) < total_expected:
        log.warning(
            "Only received %d out of %d expected results after %d attempts",
            len(scan_results),
            total_expected,
            DEFAULT_POLL_ATTEMPTS,
        )

    # Process results
    malicious_prompts = []
    benign_prompts = []
    malicious_responses = []
    benign_responses = []

    # Track violation types
    violation_types = {
        vtype: 0 for vtype in PROMPT_VIOLATION_FIELDS + RESPONSE_VIOLATION_FIELDS
    }

    log.debug("Processing %d scan results", len(scan_results))
    for idx, result in enumerate(scan_results):
        # Check if this is a ScanIdResult with a nested result
        if hasattr(result, "result") and result.result:
            scan_res = result.result
            req_id = result.req_id
            original_content = content_map.get(req_id, {})

            if idx < 5:
                log.debug(
                    "Result %d: req_id=%s, category=%s, action=%s, prompt_detected=%s, response_detected=%s",
                    idx,
                    req_id,
                    scan_res.category,
                    scan_res.action,
                    scan_res.prompt_detected,
                    scan_res.response_detected,
                )

            prompt_text = original_content.get("prompt", "N/A")
            response_text = original_content.get("response", "N/A") or "N/A"
            category = scan_res.category
            action = scan_res.action

            # Get violation details
            prompt_detected = scan_res.prompt_detected
            response_detected = scan_res.response_detected

            # Count violations
            for key in PROMPT_VIOLATION_FIELDS:
                if getattr(prompt_detected, key, False):
                    violation_types[key] += 1

            for key in RESPONSE_VIOLATION_FIELDS:
                if getattr(response_detected, key, False):
                    violation_types[key] += 1

            # Build violation lists
            prompt_violations = get_violations(prompt_detected, PROMPT_VIOLATION_FIELDS)
            response_violations = get_violations(
                response_detected, RESPONSE_VIOLATION_FIELDS
            )

            # Truncate text for display
            prompt_display = (
                prompt_text[:TEXT_TRUNCATE_LENGTH] + "..."
                if len(prompt_text) > TEXT_TRUNCATE_LENGTH
                else prompt_text
            )
            response_display = (
                response_text[:TEXT_TRUNCATE_LENGTH] + "..."
                if len(response_text) > TEXT_TRUNCATE_LENGTH
                else response_text
            )

            # Categorize based on overall scan result category
            if category == "malicious":
                # For malicious scans, add to malicious lists
                malicious_prompts.append(
                    {
                        "prompt": prompt_display,
                        "violations": ", ".join(prompt_violations)
                        if prompt_violations
                        else "policy violation",
                        "action": action,
                    }
                )
                malicious_responses.append(
                    {
                        "response": response_display,
                        "violations": ", ".join(response_violations)
                        if response_violations
                        else "policy violation",
                        "action": action,
                    }
                )
            else:
                # Benign category
                benign_prompts.append({"prompt": prompt_display, "action": action})
                benign_responses.append(
                    {"response": response_display, "action": action}
                )

    # Display results
    display_scan_results(
        malicious_prompts,
        benign_prompts,
        malicious_responses,
        benign_responses,
        violation_types,
        len(scan_results),
    )

    return {
        "malicious_prompts": malicious_prompts,
        "benign_prompts": benign_prompts,
        "malicious_responses": malicious_responses,
        "benign_responses": benign_responses,
        "violation_types": violation_types,
    }


def display_scan_results(
    malicious_prompts: List[Dict[str, Any]],
    benign_prompts: List[Dict[str, Any]],
    malicious_responses: List[Dict[str, Any]],
    benign_responses: List[Dict[str, Any]],
    violation_types: Dict[str, int],
    total_scans: int,
) -> None:
    """Display scan results in tabular format."""
    print("\n" + DIVIDER)
    print("AI RUNTIME SECURITY SCAN RESULTS".center(DISPLAY_WIDTH))
    print(DIVIDER)

    # Malicious Prompts
    if malicious_prompts:
        print(f"\n🚨 MALICIOUS PROMPTS ({len(malicious_prompts)} detected)")
        print(SUBDIV)
        headers = ["Prompt", "Violations", "Action"]
        table_data = [
            [p["prompt"], p["violations"], p["action"]] for p in malicious_prompts[:10]
        ]
        print(
            tabulate(
                table_data,
                headers=headers,
                tablefmt="rounded_outline",
                maxcolwidths=[85, 20, 10],
                numalign="left",
            )
        )
        if len(malicious_prompts) > 10:
            print(f"... and {len(malicious_prompts) - 10} more malicious prompts")

    # Benign Prompts
    if benign_prompts:
        print(f"\n✅ BENIGN PROMPTS ({len(benign_prompts)} detected)")
        print(SUBDIV)
        headers = ["Prompt", "Action"]
        table_data = [[p["prompt"], p["action"]] for p in benign_prompts[:5]]
        print(
            tabulate(
                table_data,
                headers=headers,
                tablefmt="rounded_outline",
                maxcolwidths=[105, 10],
                numalign="left",
            )
        )
        if len(benign_prompts) > 5:
            print(f"... and {len(benign_prompts) - 5} more benign prompts")

    # Malicious Responses
    if malicious_responses:
        print(f"\n🚨 MALICIOUS RESPONSES ({len(malicious_responses)} detected)")
        print(SUBDIV)
        headers = ["Response", "Violations", "Action"]
        table_data = [
            [r["response"], r["violations"], r["action"]]
            for r in malicious_responses[:10]
        ]
        print(
            tabulate(
                table_data,
                headers=headers,
                tablefmt="rounded_outline",
                maxcolwidths=[85, 20, 10],
                numalign="left",
            )
        )
        if len(malicious_responses) > 10:
            print(f"... and {len(malicious_responses) - 10} more malicious responses")

    # Benign Responses
    if benign_responses:
        print(f"\n✅ BENIGN RESPONSES ({len(benign_responses)} detected)")
        print(SUBDIV)
        headers = ["Response", "Action"]
        table_data = [[r["response"], r["action"]] for r in benign_responses[:5]]
        print(
            tabulate(
                table_data,
                headers=headers,
                tablefmt="rounded_outline",
                maxcolwidths=[105, 10],
                numalign="left",
            )
        )
        if len(benign_responses) > 5:
            print(f"... and {len(benign_responses) - 5} more benign responses")

    # Violation Types Summary
    print("\n📊 VIOLATION TYPES BREAKDOWN")
    print(SUBDIV)
    violation_data = []
    for vtype, count in violation_types.items():
        if count > 0:
            violation_data.append([vtype.replace("_", " ").title(), count])

    if violation_data:
        print(
            tabulate(
                violation_data,
                headers=["Violation Type", "Count"],
                tablefmt="rounded_outline",
                numalign="left",
            )
        )

    # Final Summary
    print("\n📈 SUMMARY")
    print(SUBDIV)
    summary_data = [
        ["Total Scans", total_scans],
        ["Malicious Prompts", len(malicious_prompts)],
        ["Benign Prompts", len(benign_prompts)],
        ["Malicious Responses", len(malicious_responses)],
        ["Benign Responses", len(benign_responses)],
    ]
    print(
        tabulate(
            summary_data,
            headers=["Metric", "Count"],
            tablefmt="rounded_outline",
            numalign="left",
        )
    )

    print("\n" + DIVIDER)


# --------------------------------------------------------------------------- #
#                                 Main entry                                  #
# --------------------------------------------------------------------------- #


def main() -> None:
    """Main entry point for the AI Runtime Security batch scanner."""
    dotenv.load_dotenv()  # safe even if .env is absent

    parser = argparse.ArgumentParser(
        description="Bulk scan prompts with AIRS (pan-aisecurity SDK)."
    )
    parser.add_argument(
        "--file", required=True, type=pathlib.Path, help="CSV, JSON, or YAML input"
    )
    parser.add_argument(
        "--output", type=pathlib.Path, help="Write raw JSON batch responses"
    )
    parser.add_argument("--profile-name", help="AI Profile name (overrides env)")
    parser.add_argument("--profile-id", help="AI Profile ID (overrides env)")
    parser.add_argument("--endpoint", help="Custom API endpoint")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"Number of items per batch (default: {DEFAULT_BATCH_SIZE})",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Root log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Shortcut for --log-level DEBUG (overrides)",
    )
    parser.add_argument(
        "--retrieve-results",
        action="store_true",
        help="Retrieve and display detailed scan results after submission",
    )
    args = parser.parse_args()

    configure_logging(args.log_level, args.debug)

    try:
        _run(args)
    except Exception as exc:  # noqa: BLE001 – surface everything
        log.fatal("Execution aborted due to an error: %s", exc, exc_info=True)
        raise  # re‑raise so a non‑zero exit code propagates


def _run(args: argparse.Namespace) -> None:
    """Run the batch scanner with the provided arguments."""
    if args.batch_size < 1:
        raise ValueError("--batch-size must be at least 1")

    api_key = os.getenv("PANW_AI_SEC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "API key missing – set PANW_AI_SEC_API_KEY in env or .env file."
        )

    aisecurity.init(
        api_key=api_key,
        api_endpoint=args.endpoint or os.getenv("PANW_AI_SEC_API_ENDPOINT"),
    )
    log.debug("SDK initialised")

    profile_name = args.profile_name or os.getenv("PANW_AI_PROFILE_NAME")
    profile_id = args.profile_id or os.getenv("PANW_AI_PROFILE_ID")
    if not (profile_name or profile_id):
        raise RuntimeError(
            "Provide --profile-name or --profile-id (or matching env var)."
        )

    ai_profile = (
        AiProfile(profile_name=profile_name)
        if profile_name
        else AiProfile(profile_id=profile_id)
    )
    log.debug("Using AI profile: %s", profile_name or profile_id)

    scan_contents = load_input_file(args.file)
    if not scan_contents:
        log.warning("Input file contained zero prompts – nothing to do.")
        return

    async_objects, content_map = build_scan_objects(scan_contents, ai_profile)

    batch_results = asyncio.run(
        run_batches(
            async_objects,
            batch_size=args.batch_size,
            endpoint_override=args.endpoint,
        )
    )
    pretty_print_batch_results(batch_results)

    # Retrieve and display detailed results if requested
    if args.retrieve_results:
        scanner = Scanner()
        if args.endpoint:
            scanner.api_endpoint = args.endpoint

        try:
            detailed_results = asyncio.run(
                retrieve_and_display_results(scanner, batch_results, content_map)
            )

            # Optionally save detailed results to output file
            if args.output:
                # Add detailed results to output
                for res, details in zip(
                    batch_results,
                    detailed_results.get("malicious", [])
                    + detailed_results.get("benign", []),
                ):
                    if hasattr(res, "detailed_results"):
                        res.detailed_results = details
        finally:
            asyncio.run(scanner.close())

    if args.output:
        with args.output.open("w", encoding="utf-8") as f:
            # Convert datetime objects to strings for JSON serialization
            results_data = []
            for res in batch_results:
                res_dict = res.to_dict()
                # Convert datetime to ISO format string
                if "received" in res_dict and hasattr(
                    res_dict["received"], "isoformat"
                ):
                    res_dict["received"] = res_dict["received"].isoformat()
                results_data.append(res_dict)
            json.dump(results_data, f, indent=2)
        log.info("Raw batch responses written to %s", args.output)


if __name__ == "__main__":
    main()
