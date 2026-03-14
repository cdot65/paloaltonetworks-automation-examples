# Jenkins on Kubernetes for PAN-OS Automation

## Overview

End-to-end framework for running PAN-OS automation pipelines on Jenkins deployed to Kubernetes. Jenkins dynamically provisions agent pods that execute Python scripts against Palo Alto Networks Panorama to configure address objects and security policies.

## Architecture

```
+---------------------+       +---------------------------+
|  Jenkins Controller |       |  Kubernetes Cluster       |
|  (Helm deployment)  |       |                           |
|                     +------>+  Dynamic Agent Pods       |
|  helm/values.yaml   |       |  +-------+ +-----------+ |
+---------------------+       |  | jnlp  | |  python   | |
                               |  | (kubectl)| (pan-os) | |
                               |  +-------+ +-----------+ |
                               |                           |
                               |  RBAC: manifests/         |
                               +---------------------------+
                                          |
                                          v
                               +---------------------------+
                               |  Panorama Appliance       |
                               |  (PAN-OS API)             |
                               +---------------------------+
```

**Flow:**

1. Jenkins controller is deployed via Helm (`helm/`).
2. RBAC manifests (`manifests/`) grant agent pods permission to operate within the cluster.
3. A pipeline job is triggered with parameters (hostname, credentials, rule/object details).
4. Jenkins Kubernetes plugin spawns an agent pod with two containers:
   - `jnlp` -- custom image (`docker/`) with kubectl, handles agent communication and git clone.
   - `python` -- `pan-os-docker` image with PAN-OS SDK, runs the automation script.
5. The Python script connects to Panorama and applies the requested configuration.

## Components

| Directory | Purpose | README |
|---|---|---|
| [docker/](docker/) | Custom Jenkins agent image with kubectl | [docker/README.md](docker/README.md) |
| [helm/](helm/) | Helm values for deploying the Jenkins controller | [helm/README.md](helm/README.md) |
| [manifests/](manifests/) | Kubernetes RBAC resources for agent pods | [manifests/README.md](manifests/README.md) |
| [pipelines/](pipelines/) | Groovy pipeline scripts for PAN-OS automation | [pipelines/README.md](pipelines/README.md) |

## Security Warning -- Hardcoded Credentials

The pipeline scripts in `pipelines/` contain hardcoded demo credentials (`officehours` / `paloalto123`). These are for demonstration purposes only.

**For any non-demo deployment**, replace inline credentials with Jenkins Credentials binding:

```groovy
withCredentials([usernamePassword(
    credentialsId: 'panorama-credentials',
    usernameVariable: 'USERNAME',
    passwordVariable: 'PASSWORD'
)]) {
    // pipeline steps here
}
```

See [pipelines/README.md](pipelines/README.md) for full instructions.

## Quick Start

```bash
# 1. Deploy Jenkins
helm repo add jenkins https://charts.jenkins.io && helm repo update
helm install jenkins jenkins/jenkins -n jenkins -f helm/values.yaml --create-namespace

# 2. Apply agent RBAC
kubectl apply -f manifests/

# 3. Build and push the custom agent image
cd docker && docker build -t ghcr.io/<your-org>/jenkins-kubectl:latest . && docker push ghcr.io/<your-org>/jenkins-kubectl:latest

# 4. Get admin password
kubectl exec -n jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/additional/chart-admin-password && echo

# 5. Create pipeline jobs in the Jenkins UI using the scripts in pipelines/
```

## Prerequisites

- Kubernetes cluster with kubectl access
- Helm 3.x
- Docker 20.10+
- Container registry access
- Network path from Kubernetes pods to the Panorama appliance
- Jenkins plugins: Kubernetes Plugin, Pipeline Utility Steps

## Resources

- [Jenkins Kubernetes Plugin](https://plugins.jenkins.io/kubernetes/)
- [Jenkins Helm Chart](https://github.com/jenkinsci/helm-charts)
- [PAN-OS Python SDK](https://github.com/PaloAltoNetworks/pan-os-python)
