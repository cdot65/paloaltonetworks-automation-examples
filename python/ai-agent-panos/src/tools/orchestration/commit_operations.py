"""Commit operations orchestration tool.

Provides commit workflow with approval gates and job polling.
"""

import uuid

from langchain_core.tools import tool


@tool
def commit_changes(
    description: str = "Changes via PAN-OS Agent",
    sync: bool = True,
    require_approval: bool = False,
) -> str:
    """Commit pending changes to PAN-OS firewall.

    Args:
        description: Commit description/message
        sync: Wait for commit to complete (True) or return immediately (False)
        require_approval: Require human approval before committing

    Returns:
        Commit operation result

    Examples:
        # Simple commit
        commit_changes(description="Added web servers")

        # Async commit (return immediately)
        commit_changes(description="Policy updates", sync=False)

        # With approval gate
        commit_changes(
            description="Critical security policy changes",
            require_approval=True
        )
    """
    from src.core.subgraphs.commit import create_commit_subgraph

    commit_graph = create_commit_subgraph()

    try:
        result = commit_graph.invoke(
            {
                "description": description,
                "sync": sync,
                "require_approval": require_approval,
                "approval_granted": None,
                "commit_job_id": None,
                "job_status": None,
                "job_result": None,
                "message": "",
                "error": None,
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
        return result["message"]
    except Exception as e:
        return f"❌ Commit error: {type(e).__name__}: {e}"
