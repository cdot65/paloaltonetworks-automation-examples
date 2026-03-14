# Jenkins Agent Docker Image

## Overview

Custom Docker image extending the official Jenkins inbound agent (`jenkins/inbound-agent:latest`) with `kubectl` pre-installed. This image is used by the Kubernetes plugin to spawn dynamic Jenkins agent pods that can interact with the Kubernetes API server during pipeline execution.

Within the broader Jenkins-on-K8s architecture, this image serves as the `jnlp` container in multi-container agent pods defined by the pipeline scripts in `../pipelines/`.

## Prerequisites

- Docker 20.10+ installed locally
- Access to a container registry (e.g., GitHub Container Registry, Docker Hub)
- Authenticated to the target registry (`docker login`)

## Quickstart

1. Clone the repository and navigate to this directory:

   ```bash
   cd jenkins/docker
   ```

2. Build the image:

   ```bash
   docker build -t ghcr.io/<your-org>/jenkins-kubectl:latest .
   ```

3. Push to your registry:

   ```bash
   docker push ghcr.io/<your-org>/jenkins-kubectl:latest
   ```

4. Update the pipeline scripts in `../pipelines/` to reference your image in the pod template YAML.

## Configuration

The Dockerfile accepts no build arguments. Key decisions are baked into the image:

| Layer | Detail |
|---|---|
| Base image | `jenkins/inbound-agent:latest` |
| User context | Switches to `root` for installs, returns to `jenkins` |
| kubectl version | Pulls the latest stable release at build time via `https://dl.k8s.io/release/stable.txt` |
| Additional packages | `apt-transport-https`, `gnupg2`, `curl`, `ca-certificates` |

To pin a specific kubectl version, replace the download URL in the Dockerfile:

```dockerfile
RUN curl -LO "https://dl.k8s.io/release/v1.28.0/bin/linux/amd64/kubectl"
```

## Usage

Verify the built image locally:

```bash
docker run --rm ghcr.io/<your-org>/jenkins-kubectl:latest kubectl version --client
```

Expected output:

```
Client Version: v1.x.x
Kustomize Version: v5.x.x
```

## Project Structure

```
docker/
  Dockerfile       # Extends jenkins/inbound-agent with kubectl
  README.md        # This file
```

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| `kubectl: command not found` inside agent pod | Image was not rebuilt or pod is using the upstream `jenkins/inbound-agent` | Verify the pipeline pod template references the custom image, not the base image |
| Build fails on `curl -fsSL https://apt.releases.hashicorp.com/gpg` | Network or DNS issue during build | Retry with `--network=host` or check proxy settings |
| `permission denied` running kubectl in pipeline | Container running as `jenkins` user without cluster RBAC | Apply the RBAC manifests from `../manifests/` and ensure the pod uses `serviceAccountName: jenkins-agent-sa` |
| Image push fails with 401 | Not authenticated to the container registry | Run `docker login ghcr.io` (or your registry) before pushing |
| kubectl version mismatch with cluster | Image pulls latest kubectl at build time; cluster may be older | Pin a specific kubectl version in the Dockerfile to match your cluster |
