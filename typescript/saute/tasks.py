"""Tasks to execute with Invoke."""

# ---------------------------------------------------------------------------
# Python3.11 hack for invoke
# ---------------------------------------------------------------------------
import inspect

if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

import os
from invoke import task

# ---------------------------------------------------------------------------
# DOCKER PARAMETERS
# ---------------------------------------------------------------------------
DOCKER_IMG_BACKEND = "ghcr.io/cdot65/saute-backend"
DOCKER_TAG_BACKEND = "0.0.1"

DOCKER_IMG_FRONTEND = "ghcr.io/cdot65/saute-frontend"
DOCKER_TAG_FRONTEND = "0.0.1"

DOCKER_IMG_WORKER = "ghcr.io/cdot65/saute-worker"
DOCKER_TAG_WORKER = "0.0.1"


# ---------------------------------------------------------------------------
# SYSTEM PARAMETERS
# ---------------------------------------------------------------------------
PWD = os.getcwd()


# ---------------------------------------------------------------------------
# DOCKER CONTAINER BUILDS
# ---------------------------------------------------------------------------
@task()
def build(context):
    """Build our Docker images."""
    backend = f"docker build -t {DOCKER_IMG_BACKEND}:{DOCKER_TAG_BACKEND} ./backend"
    worker = f"docker tag {DOCKER_IMG_BACKEND}:{DOCKER_TAG_BACKEND} {DOCKER_IMG_WORKER}:{DOCKER_TAG_WORKER}"
    frontend = f"docker build -t {DOCKER_IMG_FRONTEND}:{DOCKER_TAG_FRONTEND} ./frontend"
    context.run(
        f"{backend} && {frontend} && {worker}",
    )


# ---------------------------------------------------------------------------
# DOCKER CONTAINER IMAGE PUBLISH
# ---------------------------------------------------------------------------
@task()
def publish(context):
    """Build our Docker images."""
    backend = f"docker push {DOCKER_IMG_BACKEND}:{DOCKER_TAG_BACKEND}"
    worker = f"docker push {DOCKER_IMG_WORKER}:{DOCKER_TAG_WORKER}"
    frontend = f"docker push {DOCKER_IMG_FRONTEND}:{DOCKER_TAG_FRONTEND}"
    context.run(
        f"{backend} && {frontend} && {worker}",
    )
