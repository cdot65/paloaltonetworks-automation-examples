# Jenkins Infrastructure

Kubernetes manifests, Helm configuration, and Docker images for deploying Jenkins with dynamic agent pods.

## Components

### Docker Agent Image

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/jenkins/docker)

Custom Docker image extending `jenkins/inbound-agent` with `kubectl` pre-installed. Used as the JNLP container in multi-container Kubernetes agent pods.

```bash
cd jenkins/docker
docker build -t jenkins-agent-kubectl:latest .
```

### Helm Chart Values

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/jenkins/helm)

Values file for deploying Jenkins via the official Helm chart:

- Exposes Jenkins via LoadBalancer service
- Configures persistent storage for Jenkins home
- Sets up RBAC for Kubernetes plugin integration

```bash
helm repo add jenkins https://charts.jenkins.io
helm install jenkins jenkins/jenkins -f jenkins/helm/values.yaml
```

### RBAC Manifests

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/jenkins/manifests)

Kubernetes ServiceAccount, ClusterRole, and ClusterRoleBinding that grant dynamically spawned Jenkins agent pods permission to interact with the Kubernetes API.

```bash
kubectl apply -f jenkins/manifests/
```
