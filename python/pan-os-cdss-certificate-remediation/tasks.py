from invoke import task
import os

# ---------------------------------------------------------------------------
# DOCKER PARAMETERS
# ---------------------------------------------------------------------------
DOCKER_COMPOSE_PROJECT = "pan-os-cdss-certificate-remediation"
DOCKER_COMPOSE_FILE = "docker-compose.yaml"


def load_env():
    with open(".env") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


# ---------------------------------------------------------------------------
# DOCKER CONTAINER BUILDS
# ---------------------------------------------------------------------------
@task
def build(context):
    """Build our Docker images."""
    context.run(f"docker compose -f {DOCKER_COMPOSE_FILE} build", pty=True)


# ---------------------------------------------------------------------------
# LOCAL DEVELOPMENT INSTANCE
# ---------------------------------------------------------------------------
@task
def local(context):
    """Run container locally."""
    load_env()
    context.run(f"docker compose -f {DOCKER_COMPOSE_FILE} up", pty=True)


# ---------------------------------------------------------------------------
# SHELL ACCESS
# ---------------------------------------------------------------------------
@task
def shell(context):
    """Get shell access to the container."""
    context.run(
        f"docker compose -f {DOCKER_COMPOSE_FILE} run --rm web /bin/sh", pty=True
    )


# ---------------------------------------------------------------------------
# PYTHON
# ---------------------------------------------------------------------------
@task
def python(context):
    """Get access to the Python REPL within our container."""
    context.run(
        f"docker compose -f {DOCKER_COMPOSE_FILE} run --rm web python", pty=True
    )


# ---------------------------------------------------------------------------
# DJANGO MANAGEMENT COMMANDS
# ---------------------------------------------------------------------------
@task
def manage(context, command):
    """Run Django management commands."""
    context.run(
        f"docker compose -f {DOCKER_COMPOSE_FILE} run --rm web python manage.py {command}",
        pty=True,
    )
