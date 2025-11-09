"""
LangSmith anonymizers for masking sensitive data in traces.

This module provides anonymization patterns to prevent credential leakage
when sending traces to LangSmith. CRITICAL: All sensitive data patterns must
be masked before traces leave the application.

Patterns covered:
- PAN-OS API keys (LUFRPT... format)
- Anthropic API keys (sk-ant-... format)
- Password fields (various formats)
- XML password elements
"""

import os
from langchain_core.tracers.langchain import LangChainTracer
from langsmith import Client
from langsmith.anonymizer import create_anonymizer


def get_anonymized_langsmith_client() -> Client:
    """
    Create LangSmith client with PAN-OS-specific anonymization patterns.

    This function creates a LangSmith client that masks sensitive data:
    1. PAN-OS API keys (LUFRPT[base64 string])
    2. Anthropic API keys (sk-ant-[alphanumeric])
    3. Password fields in any format (password=, passwd=, pwd=)
    4. XML password elements (<password>...</password>)

    Returns:
        Client: LangSmith client with anonymization

    Example:
        >>> client = get_anonymized_langsmith_client()
        >>> # Client automatically anonymizes all traces

    Security:
        All patterns are applied CLIENT-SIDE before data leaves the application.
        This ensures sensitive data never reaches LangSmith servers.
    """
    anonymizer = create_anonymizer(
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

    # Create client with anonymizer
    return Client(anonymizer=anonymizer)


# Initialize global anonymized LangSmith client if tracing is enabled
if os.getenv("LANGSMITH_TRACING") == "true":
    # Set the default LangSmith client to use anonymization
    import langsmith
    langsmith.client = get_anonymized_langsmith_client()
