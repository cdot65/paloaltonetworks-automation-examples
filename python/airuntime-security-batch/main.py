#!/usr/bin/env python3
"""
airs_batch_scan.py – Bulk‑scan prompts with Palo Alto Networks
AI Runtime Security (AIRS) via the pan‑aisecurity Python SDK.

Differences from the first release:
• Rich logging with --log-level / --debug
• Correct AiProfile import path
• Clear progress breadcrumbs at INFO level
• Fatal‑level logging of any exception before exit
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import itertools
import json
import logging
import os
import pathlib
import sys
from typing import Any, Dict, List

import dotenv
import yaml  # PyYAML
import aisecurity
from aisecurity.constants.base import MAX_NUMBER_OF_BATCH_SCAN_OBJECTS
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile  # ← fixed
from aisecurity.generated_openapi_client import (
    AsyncScanObject,
    ScanRequest,
    ScanRequestContentsInner,
)
from aisecurity.scan.asyncio.scanner import Scanner

# --------------------------------------------------------------------------- #
#                               logging setup                                 #
# --------------------------------------------------------------------------- #

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
logging.basicConfig(format=LOG_FORMAT, stream=sys.stdout)
log = logging.getLogger("airs-batch-scan")


def configure_logging(level_str: str | None, debug_flag: bool) -> None:
    level = logging.DEBUG if debug_flag else logging.getLevelName(level_str or "INFO")
    logging.getLogger().setLevel(level)
    # Bridge SDK & aiohttp logs
    logging.getLogger("aisecurity").setLevel(level)
    logging.getLogger("aiohttp.client").setLevel(level)


# --------------------------------------------------------------------------- #
#                             Utility functions                               #
# --------------------------------------------------------------------------- #


def batched(iterable, n):
    """Back‑port itertools.batched for <3.12."""
    if hasattr(itertools, "batched"):  # pragma: >=3.12
        yield from itertools.batched(iterable, n)
    else:
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(itertools.islice(it, n)):
            yield batch


def load_input_file(path: pathlib.Path) -> List[Dict[str, str | None]]:
    """
    Parse CSV, JSON, or YAML into a list of {'prompt': ..., 'response': ...}.
    """
    log.info("Loading input file: %s", path)
    ext = path.suffix.lower()
    if ext == ".csv":
        with path.open(newline="", encoding="utf‑8") as f:
            reader = csv.DictReader(f)
            rows = [
                {"prompt": r.get("prompt"), "response": r.get("response")}
                for r in reader
            ]
    elif ext in (".yml", ".yaml"):
        with path.open(encoding="utf‑8") as f:
            data = yaml.safe_load(f)
        rows = _normalise_yaml_json(data)
    elif ext == ".json":
        with path.open(encoding="utf‑8") as f:
            data = json.load(f)
        rows = _normalise_yaml_json(data)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    log.debug("Loaded %d row(s) from %s", len(rows), path)
    return rows


def _normalise_yaml_json(data: Any) -> List[Dict[str, str | None]]:
    """
    Normalise YAML/JSON structures to a list[dict(prompt, response)].
    """
    if isinstance(data, dict):
        data = list(data.values())
    normalised: list[dict[str, str | None]] = []
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
    scan_contents: List[Dict[str, str | None]],
    ai_profile: AiProfile,
) -> List[AsyncScanObject]:
    async_objects: list[AsyncScanObject] = []
    req_id = 0
    for sc in scan_contents:
        req_id += 1
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
    return async_objects


async def run_batches(
    async_objects: List[AsyncScanObject],
    batch_size: int,
    endpoint_override: str | None = None,
) -> List[Any]:
    """
    Submit batches concurrently and return list of AsyncScanResponse.
    """
    scanner = Scanner()
    if endpoint_override:
        scanner.api_endpoint = endpoint_override  # type: ignore[attr-defined]

    batches = [list(batch) for batch in batched(async_objects, batch_size)]
    log.info("Submitting %d batch(es)…", len(batches))
    for i, b in enumerate(batches, 1):
        log.debug(" Batch %d: %d object(s)", i, len(b))

    coroutines = [scanner.async_scan(batch) for batch in batches]
    try:
        responses = await asyncio.gather(*coroutines)
    finally:
        await scanner.close()

    return responses


def pretty_print_batch_results(batch_results):
    for idx, res in enumerate(batch_results, start=1):
        print(
            f"[Batch {idx}]  received={res.received!s:<5}  "
            f"scan_id={res.scan_id}  report_id={res.report_id}"
        )


# --------------------------------------------------------------------------- #
#                                 Main entry                                  #
# --------------------------------------------------------------------------- #


def main() -> None:
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
        "--batch-size", type=int, default=MAX_NUMBER_OF_BATCH_SCAN_OBJECTS
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
    args = parser.parse_args()

    configure_logging(args.log_level, args.debug)

    try:
        _run(args)
    except Exception as exc:  # noqa: BLE001 – surface everything
        log.fatal("Execution aborted due to an error: %s", exc, exc_info=True)
        raise  # re‑raise so a non‑zero exit code propagates


def _run(args) -> None:
    if args.batch_size < 1 or args.batch_size > MAX_NUMBER_OF_BATCH_SCAN_OBJECTS:
        raise ValueError(f"--batch-size must be 1..{MAX_NUMBER_OF_BATCH_SCAN_OBJECTS}")

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

    async_objects = build_scan_objects(scan_contents, ai_profile)

    batch_results = asyncio.run(
        run_batches(
            async_objects,
            batch_size=args.batch_size,
            endpoint_override=args.endpoint,
        )
    )
    pretty_print_batch_results(batch_results)

    if args.output:
        with args.output.open("w", encoding="utf‑8") as f:
            # Convert datetime objects to strings for JSON serialization
            results_data = []
            for res in batch_results:
                res_dict = res.to_dict()
                # Convert datetime to ISO format string
                if "received" in res_dict and hasattr(res_dict["received"], "isoformat"):
                    res_dict["received"] = res_dict["received"].isoformat()
                results_data.append(res_dict)
            json.dump(results_data, f, indent=2)
        log.info("Raw batch responses written to %s", args.output)


if __name__ == "__main__":
    main()
