"""Configuration management for PAN-OS Agent.

Environment variables loaded from .env file using pydantic-settings.
"""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment variables.

    Attributes:
        panos_hostname: IP address or hostname of PAN-OS firewall
        panos_username: Admin username for authentication
        panos_password: Admin password for authentication
        panos_api_key: Optional API key (alternative to username/password)
        anthropic_api_key: Anthropic API key for LLM
        default_mode: Default agent mode (autonomous or deterministic)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        langsmith_api_key: LangSmith API key for logging and evaluation
        langsmith_project: LangSmith project for logging and evaluation
        langsmith_tracing: Whether to enable LangSmith tracing
        langsmith_endpoint: LangSmith endpoint for logging and evaluation
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # PAN-OS Connection
    panos_hostname: str
    panos_username: str
    panos_password: str
    panos_api_key: str | None = None

    # Anthropic
    anthropic_api_key: str

    # LangSmith Observability
    langsmith_tracing: bool = Field(
        default=False,
        description="Enable LangSmith tracing for observability",
    )
    langsmith_api_key: str | None = Field(
        default=None,
        description="LangSmith API key (starts with lsv2_pt_)",
    )
    langsmith_project: str = Field(
        default="panos-agent",
        description="LangSmith project name for organizing traces",
    )
    langsmith_endpoint: str = "https://api.smith.langchain.com"

    # Agent Configuration
    default_mode: Literal["autonomous", "deterministic"] = "autonomous"
    log_level: str = "INFO"


# Timeout constants for graph invocations
# These prevent runaway executions and ensure responsive behavior

TIMEOUT_AUTONOMOUS = 300.0  # 5 minutes for autonomous mode
"""Timeout for autonomous (ReAct) mode graph invocations.

Autonomous mode can make multiple LLM calls and tool executions in a loop.
5 minutes allows for ~10-15 ReAct iterations with typical response times.
"""

TIMEOUT_DETERMINISTIC = 600.0  # 10 minutes for deterministic mode
"""Timeout for deterministic workflow mode graph invocations.

Deterministic workflows execute predefined steps sequentially.
10 minutes allows for complex multi-step workflows with commit operations.
"""

TIMEOUT_COMMIT = 180.0  # 3 minutes for commit operations
"""Timeout for PAN-OS commit operations.

Firewall commits can take 30-120 seconds depending on configuration size.
3 minutes provides buffer for slow commits while preventing indefinite hangs.
"""


# Singleton instance
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get or create settings singleton.

    Returns:
        Settings instance with environment variables loaded
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
