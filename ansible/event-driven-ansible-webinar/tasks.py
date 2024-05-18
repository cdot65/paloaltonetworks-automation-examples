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
CONTAINER_IMG = "event-driven-ansible-node"
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
        {container_cmd} build -t {CONTAINER_IMG}:{CONTAINER_TAG} ./docker
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
    """Spin up the container.

    This command will run a new container that exposes port 5000 and runs the
    ansible-rulebook command with the rulebook and inventory specified:

        podman run -d -p 5000:5000 --name eda \
            -v $(pwd)/eda:/ansible/eda ghcr.io/cdot65/ansible-eda \
            ansible-rulebook --rulebook=rulebooks/rulebook.yaml \
            -i inventory/inventory.yaml --verbose

    You will be presented with the container ID. You can then tail the logs.
    """
    container_cmd = get_container_cmd()
    run_cmd = f"""
        {container_cmd} run --rm -d -p 5000:5000 --name ansible-eda \
        -v $(pwd)/collections:/usr/share/ansible/collections \
        -v $(pwd)/roles:/usr/share/ansible/roles \
        -v $(pwd)/plugins:/usr/share/ansible/plugins \
        -v $(pwd):/ansible/eda \
        {CONTAINER_IMG}:{CONTAINER_TAG} \
        ansible-rulebook --rulebook=rulebooks/rulebook.yaml \
        -i inventory/inventory.yaml --verbose
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
    stop_cmd = f"{container_cmd} stop eda"
    remove_cmd = f"{container_cmd} rm eda"
    context.run(
        f"{stop_cmd} && {remove_cmd}",
    )


@task()
def logs(context):
    """tail -f the container logs."""
    container_cmd = get_container_cmd()
    logs_cmd = f"{container_cmd} logs -f ansible-eda"
    context.run(
        f"{logs_cmd}",
    )


@task()
def shell(context):
    """Spin up the container and access its shell for debugging / development.

    This command will run a new container that exposes port 5000 and runs the
    ansible-rulebook command with the rulebook and inventory specified:

        podman run -it --rm \
            -v $(pwd)/eda:/ansible/eda ghcr.io/cdot65/ansible-eda \
            bash

    You will be presented with the container ID. You can then tail the logs.
    """
    container_cmd = get_container_cmd()
    run_cmd = f"""
        {container_cmd} run -d --rm --name test \
        -v $(pwd):/ansible/eda {CONTAINER_IMG}:{CONTAINER_TAG} \
        bash
        """
    exec_cmd = f"{container_cmd} exec -it test"
    context.run(
        f"{run_cmd} && {exec_cmd}",
    )
