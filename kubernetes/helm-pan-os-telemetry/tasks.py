import os
from shutil import which
from invoke import task

# ---------------------------------------------------------------------------
# CONTAINER PARAMETERS
# ---------------------------------------------------------------------------
REGISTRY_URL = "ghcr.io"
DOCKER_IMG_PANOS_EXPORTER = f"{REGISTRY_URL}/cdot65/panos-exporter"
DOCKER_TAG_PANOS_EXPORTER = "0.0.1"

DOCKER_IMG_PROMETHEUS = f"{REGISTRY_URL}/cdot65/panos-prometheus"
DOCKER_TAG_PROMETHEUS = "0.0.1"

DOCKER_IMG_GRAFANA = f"{REGISTRY_URL}/cdot65/panos-grafana"
DOCKER_TAG_GRAFANA = "0.0.1"


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
        os.environ["CONTAINER_CMD"] = "podman"
        return "podman"
    elif which("docker"):
        os.environ["CONTAINER_CMD"] = "docker"
        return "docker"
    else:
        raise EnvironmentError("Neither podman nor docker is installed.")


# ---------------------------------------------------------------------------
# CONTAINER BUILDS
# ---------------------------------------------------------------------------
@task()
def build(context):
    """Build our Docker images."""
    container_cmd = get_container_cmd()
    exporter = f"{container_cmd} build -t {DOCKER_IMG_PANOS_EXPORTER}:{DOCKER_TAG_PANOS_EXPORTER} ./containers/panos_exporter"
    grafana = f"{container_cmd} build -t {DOCKER_IMG_GRAFANA}:{DOCKER_TAG_GRAFANA} ./containers/grafana"
    prometheus = f"{container_cmd} build -t {DOCKER_IMG_PROMETHEUS}:{DOCKER_TAG_PROMETHEUS} ./containers/prometheus"
    context.run(
        f"{exporter} && {grafana} && {prometheus}",
    )


# ---------------------------------------------------------------------------
# CONTAINER IMAGE PUBLISH
# ---------------------------------------------------------------------------
@task()
def publish(context):
    """Build our Docker images."""
    container_cmd = get_container_cmd()
    exporter = (
        f"{container_cmd} push {DOCKER_IMG_PANOS_EXPORTER}:{DOCKER_TAG_PANOS_EXPORTER}"
    )
    grafana = f"{container_cmd} push {DOCKER_IMG_GRAFANA}:{DOCKER_TAG_GRAFANA}"
    prometheus = f"{container_cmd} push {DOCKER_IMG_PROMETHEUS}:{DOCKER_TAG_PROMETHEUS}"
    context.run(
        f"{exporter} && {grafana} && {prometheus}",
    )


# ---------------------------------------------------------------------------
# CONTAINER IMAGE PUBLISH
# ---------------------------------------------------------------------------
@task()
def latest(context):
    """Build our Docker images."""
    container_cmd = get_container_cmd()
    tag_exporter = f"{container_cmd} tag {DOCKER_IMG_PANOS_EXPORTER}:{DOCKER_TAG_PANOS_EXPORTER} {DOCKER_IMG_PANOS_EXPORTER}:latest"
    tag_grafana = f"{container_cmd} tag {DOCKER_IMG_GRAFANA}:{DOCKER_TAG_GRAFANA} {DOCKER_IMG_GRAFANA}:latest"
    tag_prometheus = f"{container_cmd} tag {DOCKER_IMG_PROMETHEUS}:{DOCKER_TAG_PROMETHEUS} {DOCKER_IMG_PROMETHEUS}:latest"
    publish_exporter = f"{container_cmd} push {DOCKER_IMG_PANOS_EXPORTER}:latest"
    publish_grafana = f"{container_cmd} push {DOCKER_IMG_GRAFANA}:latest"
    publish_prometheus = f"{container_cmd} push {DOCKER_IMG_PROMETHEUS}:latest"
    context.run(
        f"{tag_exporter} && {tag_grafana} && {tag_prometheus} && {publish_exporter} && {publish_grafana} && {publish_prometheus}",
    )
