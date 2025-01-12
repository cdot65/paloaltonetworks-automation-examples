"""Tasks to execute with Invoke."""

# ---------------------------------------------------------------------------
# Python3.11 hack for invoke
# ---------------------------------------------------------------------------
import inspect

if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

import os
from shutil import which
from invoke import task

# ---------------------------------------------------------------------------
# CONTAINER PARAMETERS
# ---------------------------------------------------------------------------
CONTAINER_IMG = "ghcr.io/cdot65/pan-ansible"
CONTAINER_TAG = "0.0.1"


# ---------------------------------------------------------------------------
# SYSTEM PARAMETERS
# ---------------------------------------------------------------------------
PWD = os.getcwd()


# ---------------------------------------------------------------------------
# DOCKER OR PODMAN?
# ---------------------------------------------------------------------------
def get_container_cmd():
    """Determine whether to use podman or docker."""
    if which("podman"):
        return "podman"
    elif which("docker"):
        return "docker"
    else:
        raise EnvironmentError("Neither podman nor docker is installed.")


# ---------------------------------------------------------------------------
# CONTAINER BUILDS
# ---------------------------------------------------------------------------
@task()
def build(context):
    """Build our Container image."""
    container_cmd = get_container_cmd()
    build_cmd = f"""
        {container_cmd} build -t {CONTAINER_IMG}:{CONTAINER_TAG} .
    """
    context.run(
        f"{build_cmd}",
    )


# ---------------------------------------------------------------------------
# CONTAINER IMAGE PUBLISH (are you sure? this is a huge image right now >2GB)
# ---------------------------------------------------------------------------
@task()
def publish(context):
    """Publish our container image."""
    container_cmd = get_container_cmd()
    publish_cmd = f"{container_cmd} push {CONTAINER_IMG}:{CONTAINER_TAG}"
    context.run(
        f"{publish_cmd}",
    )


# ---------------------------------------------------------------------------
# CONTAINER LIFE CYCLE
# ---------------------------------------------------------------------------
@task()
def up(context):
    """Spin up the container."""
    container_cmd = get_container_cmd()
    run_cmd = f"""
        {container_cmd} run -d -it --rm --name ansible \
        -v $(pwd):/ansible {CONTAINER_IMG}:{CONTAINER_TAG} \
        /usr/bin/zsh
        """
    context.run(
        f"{run_cmd}",
    )


@task()
def down(context):
    """Spin down the container.

    This command will stop and remove the container.
    """
    container_cmd = get_container_cmd()
    stop_cmd = f"{container_cmd} stop ansible"
    context.run(
        f"{stop_cmd}",
    )


@task()
def logs(context):
    """tail -f the container logs."""
    container_cmd = get_container_cmd()
    logs_cmd = f"{container_cmd} logs -f ansible"
    context.run(
        f"{logs_cmd}",
    )


@task()
def shell(context):
    """Spin up the container and access its shell for executing playbooks."""
    container_cmd = get_container_cmd()
    exec_cmd = f"{container_cmd} exec -it ansible /usr/bin/zsh"
    context.run(
        f"{exec_cmd}",
        pty=True,
    )
