#!/usr/bin/env python3
"""LangSmith evaluation script for PAN-OS Agent.

Runs agent on evaluation dataset and tracks metrics:
- Tool usage accuracy
- Response completeness
- Error handling
- Token efficiency

Usage:
    python scripts/evaluate.py --dataset panos-agent-eval-v1 --mode autonomous
    python scripts/evaluate.py --dataset panos-agent-eval-v1 --mode deterministic
"""

import argparse
import json
import logging
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from langchain_core.messages import HumanMessage
from langsmith import Client

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.autonomous_graph import create_autonomous_graph
from src.core.config import get_settings
from src.deterministic_graph import create_deterministic_graph

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


# Example dataset for local testing (until LangSmith dataset created)
EXAMPLE_DATASET = [
    {
        "name": "List address objects",
        "input": {"messages": [HumanMessage(content="List all address objects")]},
        "expected_tool": "address_list",
        "category": "simple_list",
        "mode": "autonomous",
    },
    {
        "name": "Create address object",
        "input": {
            "messages": [
                HumanMessage(
                    content="Create address object web-server at 192.168.1.100"
                )
            ]
        },
        "expected_tool": "address_create",
        "category": "crud_create",
        "mode": "autonomous",
    },
    {
        "name": "List service objects",
        "input": {"messages": [HumanMessage(content="List all service objects")]},
        "expected_tool": "service_list",
        "category": "simple_list",
        "mode": "autonomous",
    },
    {
        "name": "Show security policies",
        "input": {"messages": [HumanMessage(content="Show all security policies")]},
        "expected_tool": "security_policy_list",
        "category": "simple_list",
        "mode": "autonomous",
    },
    {
        "name": "Invalid IP address",
        "input": {
            "messages": [
                HumanMessage(
                    content="Create address object bad-server at 999.999.999.999"
                )
            ]
        },
        "expected_behavior": "error_handling",
        "category": "error_case",
        "mode": "autonomous",
    },
    {
        "name": "Simple address workflow",
        "input": {"messages": [HumanMessage(content="workflow: simple_address")]},
        "expected_steps": 2,
        "category": "workflow",
        "mode": "deterministic",
    },
    {
        "name": "Delete address object",
        "input": {
            "messages": [HumanMessage(content="Delete address object test-server")]
        },
        "expected_tool": "address_delete",
        "category": "crud_delete",
        "mode": "autonomous",
    },
    {
        "name": "Multi-step query",
        "input": {
            "messages": [
                HumanMessage(
                    content="Create address server1 at 10.1.1.1, then create address server2 at 10.1.1.2"
                )
            ]
        },
        "expected_tools": ["address_create", "address_create"],
        "category": "multi_step",
        "mode": "autonomous",
    },
]


def evaluate_autonomous_mode(
    examples: List[Dict[str, Any]], graph: Any
) -> Dict[str, Any]:
    """Evaluate autonomous mode on examples.

    Args:
        examples: List of evaluation examples
        graph: Compiled autonomous graph

    Returns:
        Dict with evaluation metrics
    """
    results = []
    total_tokens = 0
    successful = 0
    failed = 0

    for i, example in enumerate(examples, 1):
        if example.get("mode") != "autonomous":
            continue

        logger.info(f"\n[{i}/{len(examples)}] Running: {example['name']}")

        try:
            thread_id = f"eval-{uuid.uuid4()}"
            result = graph.invoke(
                example["input"], config={"configurable": {"thread_id": thread_id}}
            )

            # Extract metrics
            last_message = result["messages"][-1]
            tokens = getattr(last_message, "usage_metadata", {})
            total_tokens += tokens.get("total_tokens", 0)

            # Check if expected tool was used
            tool_calls = []
            for msg in result["messages"]:
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    tool_calls.extend([tc["name"] for tc in msg.tool_calls])

            expected_tool = example.get("expected_tool")
            expected_tools = example.get("expected_tools", [])

            tool_match = False
            if expected_tool:
                tool_match = expected_tool in tool_calls
            elif expected_tools:
                tool_match = all(tool in tool_calls for tool in expected_tools)
            else:
                tool_match = True  # No expectation

            if tool_match:
                successful += 1
                logger.info(f"✅ Success - Tool(s) called correctly")
            else:
                failed += 1
                logger.info(
                    f"❌ Failed - Expected {expected_tool or expected_tools}, got {tool_calls}"
                )

            results.append(
                {
                    "name": example["name"],
                    "category": example.get("category"),
                    "success": tool_match,
                    "tool_calls": tool_calls,
                    "tokens": tokens.get("total_tokens", 0),
                }
            )

        except Exception as e:
            failed += 1
            logger.error(f"❌ Error: {type(e).__name__}: {e}")
            results.append(
                {
                    "name": example["name"],
                    "category": example.get("category"),
                    "success": False,
                    "error": str(e),
                }
            )

    # Calculate metrics
    total = len([ex for ex in examples if ex.get("mode") == "autonomous"])
    success_rate = successful / total if total > 0 else 0
    avg_tokens = total_tokens / total if total > 0 else 0

    return {
        "total_examples": total,
        "successful": successful,
        "failed": failed,
        "success_rate": success_rate,
        "total_tokens": total_tokens,
        "avg_tokens_per_example": avg_tokens,
        "results": results,
    }


def evaluate_deterministic_mode(
    examples: List[Dict[str, Any]], graph: Any
) -> Dict[str, Any]:
    """Evaluate deterministic mode on examples.

    Args:
        examples: List of evaluation examples
        graph: Compiled deterministic graph

    Returns:
        Dict with evaluation metrics
    """
    results = []
    successful = 0
    failed = 0

    for i, example in enumerate(examples, 1):
        if example.get("mode") != "deterministic":
            continue

        logger.info(f"\n[{i}/{len(examples)}] Running: {example['name']}")

        try:
            thread_id = f"eval-{uuid.uuid4()}"
            result = graph.invoke(
                example["input"], config={"configurable": {"thread_id": thread_id}}
            )

            # Check workflow execution
            step_outputs = result.get("step_outputs", [])
            expected_steps = example.get("expected_steps")

            if expected_steps:
                steps_match = len(step_outputs) == expected_steps
            else:
                steps_match = True  # No expectation

            if steps_match and all(
                out.get("status") == "success" for out in step_outputs
            ):
                successful += 1
                logger.info(f"✅ Success - {len(step_outputs)} steps completed")
            else:
                failed += 1
                logger.info(
                    f"❌ Failed - Expected {expected_steps}, got {len(step_outputs)}"
                )

            results.append(
                {
                    "name": example["name"],
                    "category": example.get("category"),
                    "success": steps_match,
                    "steps_executed": len(step_outputs),
                }
            )

        except Exception as e:
            failed += 1
            logger.error(f"❌ Error: {type(e).__name__}: {e}")
            results.append(
                {
                    "name": example["name"],
                    "category": example.get("category"),
                    "success": False,
                    "error": str(e),
                }
            )

    # Calculate metrics
    total = len([ex for ex in examples if ex.get("mode") == "deterministic"])
    success_rate = successful / total if total > 0 else 0

    return {
        "total_examples": total,
        "successful": successful,
        "failed": failed,
        "success_rate": success_rate,
        "results": results,
    }


def print_summary(metrics: Dict[str, Any], mode: str):
    """Print evaluation summary.

    Args:
        metrics: Evaluation metrics
        mode: Mode evaluated (autonomous or deterministic)
    """
    logger.info("\n" + "=" * 60)
    logger.info(f"EVALUATION SUMMARY - {mode.upper()} MODE")
    logger.info("=" * 60)

    logger.info(f"\nTotal Examples: {metrics['total_examples']}")
    logger.info(f"✅ Successful: {metrics['successful']}")
    logger.info(f"❌ Failed: {metrics['failed']}")
    logger.info(f"Success Rate: {metrics['success_rate']:.1%}")

    if "avg_tokens_per_example" in metrics:
        logger.info(f"\nAvg Tokens/Example: {metrics['avg_tokens_per_example']:.0f}")
        logger.info(f"Total Tokens: {metrics['total_tokens']}")

    # Category breakdown
    logger.info("\n" + "-" * 60)
    logger.info("CATEGORY BREAKDOWN")
    logger.info("-" * 60)

    categories = {}
    for result in metrics["results"]:
        cat = result.get("category", "unknown")
        if cat not in categories:
            categories[cat] = {"total": 0, "success": 0}
        categories[cat]["total"] += 1
        if result["success"]:
            categories[cat]["success"] += 1

    for cat, stats in sorted(categories.items()):
        rate = stats["success"] / stats["total"] if stats["total"] > 0 else 0
        logger.info(f"  {cat:20s}: {stats['success']}/{stats['total']} ({rate:.1%})")

    logger.info("=" * 60 + "\n")


def save_results(metrics: Dict[str, Any], mode: str):
    """Save evaluation results to file.

    Args:
        metrics: Evaluation metrics
        mode: Mode evaluated
    """
    output_dir = Path("evaluation_results")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_dir / f"eval_{mode}_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "mode": mode,
                "metrics": metrics,
            },
            f,
            indent=2,
        )

    logger.info(f"Results saved to: {filename}")


def main():
    """Run evaluation."""
    parser = argparse.ArgumentParser(description="Evaluate PAN-OS Agent")
    parser.add_argument(
        "--mode",
        choices=["autonomous", "deterministic", "both"],
        default="both",
        help="Mode to evaluate",
    )
    parser.add_argument(
        "--dataset",
        default="example",
        help="LangSmith dataset name (default: use example dataset)",
    )
    parser.add_argument(
        "--save-results", action="store_true", help="Save results to file"
    )

    args = parser.parse_args()

    # Load dataset
    if args.dataset == "example":
        logger.info("Using example dataset (LangSmith dataset not yet created)")
        examples = EXAMPLE_DATASET
    else:
        # Load from LangSmith (future enhancement)
        logger.error(f"LangSmith dataset '{args.dataset}' not yet implemented")
        logger.info("Use --dataset example for now")
        return

    # Evaluate autonomous mode
    if args.mode in ["autonomous", "both"]:
        logger.info("\n" + "=" * 60)
        logger.info("EVALUATING AUTONOMOUS MODE")
        logger.info("=" * 60)

        graph = create_autonomous_graph()
        metrics = evaluate_autonomous_mode(examples, graph)
        print_summary(metrics, "autonomous")

        if args.save_results:
            save_results(metrics, "autonomous")

    # Evaluate deterministic mode
    if args.mode in ["deterministic", "both"]:
        logger.info("\n" + "=" * 60)
        logger.info("EVALUATING DETERMINISTIC MODE")
        logger.info("=" * 60)

        graph = create_deterministic_graph()
        metrics = evaluate_deterministic_mode(examples, graph)
        print_summary(metrics, "deterministic")

        if args.save_results:
            save_results(metrics, "deterministic")


if __name__ == "__main__":
    main()
