"""CLI commands for PAN-OS agent.

Typer-based CLI for running autonomous and deterministic modes.
"""

import logging
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler

from langchain_core.messages import HumanMessage

app = typer.Typer(
    name="panos-agent",
    help="AI agent for PAN-OS firewall automation",
    add_completion=False,
)
console = Console()


def setup_logging(log_level: str = "INFO"):
    """Setup logging with rich handler."""
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )


@app.command()
def run(
    prompt: str = typer.Option(..., "--prompt", "-p", help="User prompt for the agent"),
    mode: str = typer.Option("autonomous", "--mode", "-m", help="Agent mode (autonomous or deterministic)"),
    thread_id: Optional[str] = typer.Option(None, "--thread-id", "-t", help="Thread ID for conversation continuity"),
    log_level: str = typer.Option("INFO", "--log-level", "-l", help="Logging level"),
):
    """Run PAN-OS agent with specified mode and prompt.

    Examples:
        # Autonomous mode (natural language)
        panos-agent run -p "List all address objects" -m autonomous
        panos-agent run -p "Create address object web-server at 10.1.1.100"

        # Deterministic mode (predefined workflows)
        panos-agent run -p "simple_address" -m deterministic
        panos-agent run -p "web_server_setup" -m deterministic
        panos-agent list-workflows  # See all available workflows
    """
    setup_logging(log_level)

    console.print(f"\n[bold cyan]PAN-OS Agent[/bold cyan] - Mode: {mode}")
    console.print(f"[dim]Prompt: {prompt}[/dim]\n")

    try:
        if mode == "autonomous":
            from src.autonomous_graph import create_autonomous_graph

            graph = create_autonomous_graph()

            # Use provided thread_id or generate new one
            import uuid

            tid = thread_id or str(uuid.uuid4())

            # Invoke graph
            result = graph.invoke(
                {"messages": [HumanMessage(content=prompt)]},
                config={"configurable": {"thread_id": tid}},
            )

            # Print response
            last_message = result["messages"][-1]
            console.print(f"\n[bold green]Response:[/bold green]")
            console.print(last_message.content)

            console.print(f"\n[dim]Thread ID: {tid}[/dim]")

        elif mode == "deterministic":
            from src.deterministic_graph import create_deterministic_graph

            graph = create_deterministic_graph()

            # Use provided thread_id or generate new one
            import uuid

            tid = thread_id or str(uuid.uuid4())

            # Format prompt as workflow invocation
            # Expected format: "workflow: <workflow_name>"
            if not prompt.lower().startswith("workflow:"):
                # Assume prompt is workflow name
                formatted_prompt = f"workflow: {prompt}"
            else:
                formatted_prompt = prompt

            # Invoke graph
            result = graph.invoke(
                {"messages": [HumanMessage(content=formatted_prompt)]},
                config={"configurable": {"thread_id": tid}},
            )

            # Print response
            last_message = result["messages"][-1]
            console.print(f"\n[bold green]Response:[/bold green]")
            console.print(last_message.content if isinstance(last_message, dict) else last_message.content)

            console.print(f"\n[dim]Thread ID: {tid}[/dim]")

        else:
            console.print(f"[bold red]Error:[/bold red] Unknown mode '{mode}'")
            sys.exit(1)

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {type(e).__name__}: {e}")
        logging.exception("Failed to run agent")
        sys.exit(1)


@app.command()
def studio():
    """Start LangGraph Studio server.

    Opens LangGraph Studio for visual debugging and execution.
    """
    console.print("[bold cyan]Starting LangGraph Studio...[/bold cyan]")
    console.print("[dim]This will run 'langgraph dev' in the current directory[/dim]\n")

    import subprocess

    try:
        subprocess.run(["langgraph", "dev"], check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"\n[bold red]Error:[/bold red] Failed to start LangGraph Studio")
        console.print("[dim]Make sure 'langgraph' CLI is installed: pip install langgraph-cli[/dim]")
        sys.exit(1)
    except FileNotFoundError:
        console.print(f"\n[bold red]Error:[/bold red] 'langgraph' command not found")
        console.print("[dim]Install it with: pip install langgraph-cli[/dim]")
        sys.exit(1)


@app.command()
def test_connection():
    """Test PAN-OS firewall connection.

    Verifies credentials and connectivity to the firewall.
    """
    setup_logging()

    console.print("[bold cyan]Testing PAN-OS connection...[/bold cyan]\n")

    try:
        from src.core.client import test_connection

        success, message = test_connection()

        if success:
            console.print(f"[bold green]{message}[/bold green]")
        else:
            console.print(f"[bold red]{message}[/bold red]")
            sys.exit(1)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {type(e).__name__}: {e}")
        logging.exception("Connection test failed")
        sys.exit(1)


@app.command()
def list_workflows():
    """List all available deterministic workflows.

    Shows workflow names and descriptions.
    """
    console.print("[bold cyan]Available Workflows[/bold cyan]\n")

    try:
        from src.workflows.definitions import WORKFLOWS

        if not WORKFLOWS:
            console.print("[yellow]No workflows defined[/yellow]")
            return

        for name, workflow in WORKFLOWS.items():
            console.print(f"[bold green]{name}[/bold green]")
            console.print(f"  {workflow.get('description', 'No description')}")
            console.print(f"  Steps: {len(workflow.get('steps', []))}")
            console.print()

        console.print(f"[dim]Total: {len(WORKFLOWS)} workflows[/dim]")
        console.print(f"\n[dim]Run with: panos-agent run -m deterministic -p <workflow_name>[/dim]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {type(e).__name__}: {e}")
        sys.exit(1)


@app.command()
def version():
    """Show PAN-OS agent version."""
    console.print("[bold cyan]PAN-OS Agent[/bold cyan] v0.1.0")
    console.print("[dim]LangGraph-based AI automation for PAN-OS firewalls[/dim]")


if __name__ == "__main__":
    app()
