"""Checkpoint manager for persistent SQLite storage.

Provides utilities for managing LangGraph checkpoints with SQLite backend.
"""

import logging
import sqlite3
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

logger = logging.getLogger(__name__)


def get_checkpoint_db_path() -> Path:
    """Get path to checkpoint database file.

    Returns:
        Path to checkpoints.db in data/ directory
    """
    # Get project root (3 levels up from this file)
    project_root = Path(__file__).parent.parent.parent
    db_path = project_root / "data" / "checkpoints.db"
    return db_path


def ensure_checkpoint_db_exists() -> None:
    """Ensure checkpoint database directory exists."""
    db_path = get_checkpoint_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Checkpoint database path: {db_path}")


def get_checkpointer() -> SqliteSaver:
    """Get SQLite checkpointer instance.

    Creates persistent checkpoint storage in data/checkpoints.db.
    Checkpoints survive application restarts and enable:
    - Resume from failures
    - Time-travel debugging
    - Checkpoint history inspection

    Returns:
        SqliteSaver instance configured for persistent storage

    Example:
        >>> checkpointer = get_checkpointer()
        >>> graph = workflow.compile(checkpointer=checkpointer)
    """
    ensure_checkpoint_db_exists()
    db_path = get_checkpoint_db_path()

    # Create SQLite connection for persistent storage
    # check_same_thread=False allows connection to be used across threads
    conn = sqlite3.connect(str(db_path), check_same_thread=False)

    # Create SqliteSaver instance with the connection
    checkpointer = SqliteSaver(conn=conn)

    logger.info(f"Initialized persistent checkpointer: {db_path}")
    return checkpointer
