"""Tasks to execute with Invoke."""

# ---------------------------------------------------------------------------
# standard library
# ---------------------------------------------------------------------------
import inspect
import os
import subprocess
from typing import Literal

# ---------------------------------------------------------------------------
# third party
# ---------------------------------------------------------------------------
from invoke import task

# ---------------------------------------------------------------------------
# Python3.11 hack for invoke
# ---------------------------------------------------------------------------
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec


# ---------------------------------------------------------------------------
# Determine Host operating system (to use Docker or Podman)
# ---------------------------------------------------------------------------
def get_container_runtime() -> Literal["podman", "docker"]:
    """Determine whether to use Docker or Podman based on the OS."""
    try:
        # Try to get OS information using /etc/os-release
        with open("/etc/os-release", "r") as f:
            os_release = f.read().lower()
        if any(
            operating_system in os_release
            for operating_system in ["rhel", "fedora", "centos"]
        ):
            return "podman"
    except FileNotFoundError:
        # If /etc/os-release doesn't exist, fallback to checking commands
        pass

    # Check if podman command exists
    if (
        subprocess.run(["which", "podman"], capture_output=True, text=True).returncode
        == 0
    ):
        return "podman"

    # Default to docker
    return "docker"


# ---------------------------------------------------------------------------
# ENVIRONMENT PARAMETERS
# ---------------------------------------------------------------------------
CONTAINER_RUNTIME = get_container_runtime()

# ---------------------------------------------------------------------------
# SYSTEM PARAMETERS
# ---------------------------------------------------------------------------
PWD = os.getcwd()


# ---------------------------------------------------------------------------
# CONTAINER BUILDS
# ---------------------------------------------------------------------------
@task()
def build(context):
    """Build our Container images."""
    build_containers = f"{CONTAINER_RUNTIME} compose -f docker-compose.local.yml build"
    restart_containers = (
        f"{CONTAINER_RUNTIME} compose -f docker-compose.local.yml restart"
    )
    context.run(f"{build_containers} && " f"{restart_containers}")


@task()
def rebuild(context):
    """Rebuild our Container images."""
    stop_containers = f"{CONTAINER_RUNTIME} compose -f docker-compose.local.yml" " stop"
    remove_containers = (
        f"{CONTAINER_RUNTIME} compose -f docker-compose.local.yml rm -f -v"
    )
    remove_volumes = (
        f"{CONTAINER_RUNTIME} volume rm cdss_certificate_remediation_postgres_backups "
        f"cdss_certificate_remediation_postgres_data cdss_certificate_remediation_redis_data -f"
    )
    build_containers = f"{CONTAINER_RUNTIME} compose -f docker-compose.local.yml build"
    start_containers = f"{CONTAINER_RUNTIME} compose -f docker-compose.local.yml up -d"
    # collect_static = (
    #     f"{CONTAINER_RUNTIME} compose -f docker-compose.local.yml run --rm django python manage.py "
    #     f"collectstatic --no-input"
    # )
    # create_superuser = (
    #     f"{CONTAINER_RUNTIME} compose -f docker-compose.local.yml run --rm django python manage.py "
    #     f"createsuperuser --username admin --email admin@localhost"
    # )
    context.run(
        f"{stop_containers} && "
        f"{remove_containers} && "
        f"{remove_volumes} && "
        f"{build_containers} && "
        f"{start_containers}"
    )


# Runtime Commands
@task()
def logs(context):
    """Tail the logs from our Container images."""
    tail_logs = f"{CONTAINER_RUNTIME} compose -f docker-compose.local.yml logs -f"
    context.run(f"{tail_logs}")
