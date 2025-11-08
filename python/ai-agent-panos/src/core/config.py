"""Configuration management for PAN-OS Agent.

Environment variables loaded from .env file using pydantic-settings.
"""

from typing import Literal
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

    # Agent Configuration
    default_mode: Literal["autonomous", "deterministic"] = "autonomous"
    log_level: str = "INFO"


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
