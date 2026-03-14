"""CLI commands for checkpoint management.

Provides utilities for inspecting and managing LangGraph checkpoints.
"""

import logging
from datetime import datetime
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from src.core.checkpoint_manager import get_checkpointer

logger = logging.getLogger(__name__)
console = Console()

app = typer.Typer(
    name="checkpoints",
    help="Manage LangGraph checkpoints",
    no_args_is_help=True,
)


@app.command(name="list")
def list_checkpoints(
    limit: int = typer.Option(20, "--limit", "-n", help="Maximum number of threads to show"),
):
    """List all checkpoint threads."""
    try:
        checkpointer = get_checkpointer()
        conn = checkpointer.conn
        cursor = conn.cursor()

        # Query distinct thread_ids with their latest checkpoint
        # SqliteSaver stores thread_id directly in checkpoints table
        query = """
            SELECT DISTINCT
                thread_id,
                checkpoint_id,
                MAX(checkpoint_id) as latest_checkpoint
            FROM checkpoints
            WHERE thread_id IS NOT NULL AND thread_id != ''
            GROUP BY thread_id
            ORDER BY latest_checkpoint DESC
            LIMIT ?
        """

        cursor.execute(query, (limit,))
        rows = cursor.fetchall()

        if not rows:
            console.print("No checkpoints found.", style="yellow")
            return

        # Create table
        table = Table(title=f"Checkpoint Threads ({len(rows)} threads)")
        table.add_column("Thread ID", style="cyan")
        table.add_column("Latest Checkpoint ID", style="green")
        table.add_column("Checkpoints", style="magenta")

        for thread_id, checkpoint_id, latest_checkpoint in rows:
            # Count checkpoints for this thread
            cursor.execute(
                "SELECT COUNT(*) FROM checkpoints WHERE thread_id = ?",
                (thread_id,)
            )
            count = cursor.fetchone()[0]

            table.add_row(
                thread_id or "N/A",
                latest_checkpoint or "N/A",
                str(count),
            )

        console.print(table)

    except Exception as e:
        console.print(f"❌ Error listing checkpoints: {e}", style="red")
        logger.error(f"Failed to list checkpoints: {e}", exc_info=True)
        raise typer.Exit(1)


@app.command()
def show(
    thread_id: str = typer.Argument(..., help="Thread ID to inspect"),
):
    """Show details for a specific checkpoint thread."""
    try:
        checkpointer = get_checkpointer()

        # Get checkpoint for thread
        from langgraph.checkpoint.base import CheckpointTuple

        config = {"configurable": {"thread_id": thread_id}}
        checkpoint_tuple: CheckpointTuple = checkpointer.get_tuple(config)

        if not checkpoint_tuple:
            console.print(f"❌ No checkpoint found for thread: {thread_id}", style="red")
            raise typer.Exit(1)

        # Display checkpoint info
        console.print(f"\n[bold cyan]Checkpoint Details[/bold cyan]")
        console.print(f"Thread ID: {thread_id}")
        console.print(f"Checkpoint ID: {checkpoint_tuple.checkpoint['id']}")
        console.print(f"Timestamp: {checkpoint_tuple.checkpoint.get('ts', 'N/A')}")

        # Show channel values (state)
        console.print(f"\n[bold cyan]State Channels:[/bold cyan]")
        for key, value in checkpoint_tuple.checkpoint.get("channel_values", {}).items():
            value_type = type(value).__name__
            console.print(f"  {key}: {value_type}")
            if key == "messages" and hasattr(value, '__len__'):
                try:
                    console.print(f"    Message count: {len(value)}")
                except:
                    pass

        # Show metadata if available
        if checkpoint_tuple.metadata:
            console.print(f"\n[bold cyan]Metadata:[/bold cyan]")
            for key, value in checkpoint_tuple.metadata.items():
                console.print(f"  {key}: {value}")

    except Exception as e:
        console.print(f"❌ Error showing checkpoint: {e}", style="red")
        logger.error(f"Failed to show checkpoint: {e}", exc_info=True)
        raise typer.Exit(1)


@app.command(name="history")
def show_history(
    thread_id: str = typer.Argument(..., help="Thread ID to show history for"),
    limit: int = typer.Option(10, "--limit", "-n", help="Maximum number of checkpoints to show"),
):
    """Show checkpoint history for a thread."""
    try:
        checkpointer = get_checkpointer()

        config = {"configurable": {"thread_id": thread_id}}

        # Get checkpoint history using builtin list()
        history_items = __builtins__['list'](checkpointer.list(config, limit=limit))

        if not history_items:
            console.print(f"No checkpoint history found for thread: {thread_id}", style="yellow")
            return

        # Create table
        table = Table(title=f"Checkpoint History for {thread_id}")
        table.add_column("Checkpoint ID", style="green")
        table.add_column("Timestamp", style="magenta")
        table.add_column("Step", style="cyan")

        for checkpoint_tuple in history_items:
            checkpoint = checkpoint_tuple.checkpoint

            # Format timestamp
            timestamp = checkpoint.get("ts", "N/A")
            try:
                if isinstance(timestamp, str):
                    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    formatted_time = str(timestamp)
            except Exception:
                formatted_time = str(timestamp)

            # Get step info from metadata
            step = str(checkpoint_tuple.metadata.get("step", "N/A"))

            table.add_row(
                checkpoint["id"],
                formatted_time,
                step,
            )

        console.print(table)

    except Exception as e:
        console.print(f"❌ Error showing history: {e}", style="red")
        logger.error(f"Failed to show history: {e}", exc_info=True)
        raise typer.Exit(1)


@app.command()
def delete(
    thread_id: str = typer.Argument(..., help="Thread ID to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete all checkpoints for a specific thread."""
    try:
        # Confirm deletion unless --force
        if not force:
            confirm = typer.confirm(f"Delete all checkpoints for thread '{thread_id}'?")
            if not confirm:
                console.print("Cancelled.", style="yellow")
                return

        checkpointer = get_checkpointer()
        conn = checkpointer.conn
        cursor = conn.cursor()

        # Delete checkpoints for this thread
        cursor.execute(
            "DELETE FROM checkpoints WHERE thread_id = ?",
            (thread_id,)
        )
        deleted_count = cursor.rowcount

        # Delete associated writes
        cursor.execute(
            "DELETE FROM writes WHERE thread_id = ?",
            (thread_id,)
        )

        conn.commit()

        if deleted_count > 0:
            console.print(
                f"✅ Deleted {deleted_count} checkpoint(s) for thread: {thread_id}",
                style="green"
            )
        else:
            console.print(f"No checkpoints found for thread: {thread_id}", style="yellow")

    except Exception as e:
        console.print(f"❌ Error deleting checkpoints: {e}", style="red")
        logger.error(f"Failed to delete checkpoints: {e}", exc_info=True)
        raise typer.Exit(1)


@app.command(name="prune")
def prune_old(
    days: int = typer.Option(30, "--days", "-d", help="Delete checkpoints older than N days"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete old checkpoints to free up space."""
    try:
        # Confirm pruning unless --force
        if not force:
            confirm = typer.confirm(f"Delete checkpoints older than {days} days?")
            if not confirm:
                console.print("Cancelled.", style="yellow")
                return

        checkpointer = get_checkpointer()
        conn = checkpointer.conn
        cursor = conn.cursor()

        # Calculate cutoff timestamp
        from datetime import timedelta, timezone
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        # Get all thread_ids
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints WHERE thread_id IS NOT NULL")
        thread_ids = [row[0] for row in cursor.fetchall()]

        # For each thread, get checkpoints and filter by age
        checkpoints_to_delete = []

        for thread_id in thread_ids:
            config = {"configurable": {"thread_id": thread_id}}

            # Get all checkpoints for this thread
            for checkpoint_tuple in checkpointer.list(config):
                checkpoint_ts = checkpoint_tuple.checkpoint.get("ts")

                if checkpoint_ts:
                    try:
                        # Parse timestamp
                        if isinstance(checkpoint_ts, str):
                            ts = datetime.fromisoformat(checkpoint_ts.replace("Z", "+00:00"))
                        else:
                            ts = checkpoint_ts

                        # Check if older than cutoff
                        if ts < cutoff:
                            checkpoints_to_delete.append((thread_id, checkpoint_tuple.checkpoint["id"]))
                    except Exception as e:
                        logger.debug(f"Error parsing timestamp for checkpoint: {e}")
                        continue

        # Delete old checkpoints
        deleted_count = 0
        for thread_id, checkpoint_id in checkpoints_to_delete:
            cursor.execute(
                "DELETE FROM checkpoints WHERE thread_id = ? AND checkpoint_id = ?",
                (thread_id, checkpoint_id)
            )
            deleted_count += cursor.rowcount

        # Delete orphaned writes
        cursor.execute(
            """
            DELETE FROM writes
            WHERE thread_id NOT IN (SELECT DISTINCT thread_id FROM checkpoints)
            """
        )

        conn.commit()

        if deleted_count > 0:
            console.print(
                f"✅ Pruned {deleted_count} checkpoint(s) older than {days} days",
                style="green"
            )
        else:
            console.print(f"No checkpoints older than {days} days found.", style="yellow")

        # Show database size
        import os
        from src.core.checkpoint_manager import get_checkpoint_db_path

        db_path = get_checkpoint_db_path()
        if db_path.exists():
            size_mb = os.path.getsize(db_path) / (1024 * 1024)
            console.print(f"Database size: {size_mb:.2f} MB")

    except Exception as e:
        console.print(f"❌ Error pruning checkpoints: {e}", style="red")
        logger.error(f"Failed to prune checkpoints: {e}", exc_info=True)
        raise typer.Exit(1)
