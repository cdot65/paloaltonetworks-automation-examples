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

from langchain_core.tracers.langchain import LangChainTracer
from langsmith import Client
from langsmith.anonymizer import create_anonymizer


def create_panos_anonymizer() -> LangChainTracer:
    """
    Create LangSmith tracer with PAN-OS-specific anonymization patterns.

    This function creates an anonymizer that masks:
    1. PAN-OS API keys (LUFRPT[base64 string])
    2. Anthropic API keys (sk-ant-[alphanumeric])
    3. Password fields in any format (password=, passwd=, pwd=)
    4. XML password elements (<password>...</password>)

    Returns:
        LangChainTracer: Configured tracer with anonymization patterns

    Example:
        >>> tracer = create_panos_anonymizer()
        >>> # Use tracer in LangSmith configuration

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
    tracer_client = Client(anonymizer=anonymizer)

    # Return configured tracer
    return LangChainTracer(client=tracer_client)
