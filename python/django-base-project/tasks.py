"""Tasks for use with Invoke.

(c) 2023 Calvin Remsburg
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from invoke import task

# ---------------------------------------------------------------------------
# DOCKER PARAMETERS
# ---------------------------------------------------------------------------
DOCKER_IMG = "ghcr.io/cdot65/spice-rack"
DOCKER_TAG = "0.0.1"

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
    context.run(
        f"docker build -t {DOCKER_IMG}:{DOCKER_TAG} docker",
    )


# ---------------------------------------------------------------------------
# LOCAL DEVELOPMENT INSTANCE
# ---------------------------------------------------------------------------
@task()
def local(context):
    """Run container locally."""
    context.run(
        f'docker run -it --rm \
            --mount type=bind,source="$(pwd)"/django,target=/home/django \
            -w /home/django/ \
            {DOCKER_IMG}:{DOCKER_TAG} python manage.py runserver 0.0.0.0:8000',
        pty=True,
    )


# ---------------------------------------------------------------------------
# SHELL ACCESS
# ---------------------------------------------------------------------------
@task()
def shell(context):
    """Get shell access to the container."""
    context.run(
        f'docker run -it --rm \
            --mount type=bind,source="$(pwd)"/django,target=/home/django \
            -w /home/django/ \
            {DOCKER_IMG}:{DOCKER_TAG} /bin/sh',
        pty=True,
    )


# ---------------------------------------------------------------------------
# PYTHON
# ---------------------------------------------------------------------------
@task
def python(context):
    """Get access to the ipython REPL within our container."""
    context.run(
        f'docker run -it --rm \
            --mount type=bind,source="$(pwd)"/django,target=/home/django \
            -w /home/django/ \
            {DOCKER_IMG}:{DOCKER_TAG}',
        pty=True,
    )
