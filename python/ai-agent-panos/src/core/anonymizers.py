"""
LangSmith anonymizers for masking sensitive data in traces.

This module provides anonymization patterns to prevent credential leakage
when sending traces to LangSmith.

Patterns covered:
- PAN-OS API keys (LUFRPT... format)
- Anthropic API keys (sk-ant-... format)
- Password fields (various formats)
- XML password elements
"""

from langsmith.anonymizer import create_anonymizer


def get_panos_anonymizer():
    """
    Create anonymizer with PAN-OS-specific patterns.

    Returns:
        Anonymizer: Configured anonymizer function
    """
    return create_anonymizer(
        [
            # Pattern 1: PAN-OS API keys (LUFRPT format)
            {"pattern": r"LUFRPT[A-Za-z0-9+/=]{40,}", "replace": "<panos-api-key>"},
            # Pattern 2: Anthropic API keys
            {"pattern": r"sk-ant-[A-Za-z0-9-_]{40,}", "replace": "<anthropic-api-key>"},
            # Pattern 3: Password fields
            {
                "pattern": r"(password|passwd|pwd)['\"]?\s*[:=]\s*['\"]?[^\s'\"]+",
                "replace": r"\1: <password>",
            },
            # Pattern 4: XML password elements
            {"pattern": r"<password>.*?</password>", "replace": "<password><redacted></password>"},
        ]
    )
