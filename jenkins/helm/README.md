# Jenkins Helm Deployment

## Overview

Helm values file for deploying the Jenkins controller onto a Kubernetes cluster using the official [Jenkins Helm chart](https://github.com/jenkinsci/helm-charts). This configuration exposes Jenkins via a LoadBalancer service, enables persistent storage, and creates the necessary RBAC and ServiceAccount resources for the controller itself.

Within the broader architecture, this component deploys the Jenkins controller. Agent-level RBAC is handled separately by the manifests in `../manifests/`, and the agent pod templates are defined inline within the pipeline scripts in `../pipelines/`.

## Prerequisites

- Kubernetes cluster with `kubectl` access
- Helm 3.x installed
- A storage class available in the cluster (default assumes `local-path` from k3s)
- A free IP address for the LoadBalancer (or remove `loadBalancerIP` to auto-assign)

## Quickstart

1. Add the Jenkins Helm repository:

   ```bash
   helm repo add jenkins https://charts.jenkins.io
   helm repo update
   ```

2. Review and edit `values.yaml` -- at minimum, update `loadBalancerIP`:

   ```bash
   vi jenkins/helm/values.yaml
   ```

3. Install Jenkins into the `jenkins` namespace:

   ```bash
   helm install jenkins jenkins/jenkins \
     --namespace jenkins \
     -f jenkins/helm/values.yaml \
     --create-namespace
   ```

4. Wait for the pod to become ready:

   ```bash
   kubectl get pods -n jenkins -w
   ```

5. Retrieve the admin password:

   ```bash
   kubectl exec -n jenkins -it svc/jenkins -c jenkins -- \
     /bin/cat /run/secrets/additional/chart-admin-password && echo
   ```

6. Access Jenkins at `http://<LOAD_BALANCER_IP>:8080`.

## Configuration

All settings are in `values.yaml`. Key parameters:

| Key | Default | Description |
|---|---|---|
| `controller.serviceType` | `LoadBalancer` | How the Jenkins UI is exposed. Alternatives: `ClusterIP`, `NodePort` |
| `controller.loadBalancerIP` | `172.16.0.75` | Static IP for the LoadBalancer. Remove to auto-assign |
| `controller.ingress.enabled` | `false` | Set to `true` and configure annotations if using an Ingress controller instead |
| `controller.resources.requests.cpu` | `500m` | CPU request for the controller pod |
| `controller.resources.requests.memory` | `1024Mi` | Memory request for the controller pod |
| `controller.resources.limits.cpu` | `2000m` | CPU limit for the controller pod |
| `controller.resources.limits.memory` | `4096Mi` | Memory limit for the controller pod |
| `persistence.enabled` | `true` | Persist Jenkins home across pod restarts |
| `persistence.storageClass` | `local-path` | Storage class name. Change to match your cluster |
| `persistence.size` | `20Gi` | PVC size for Jenkins home |
| `rbac.create` | `true` | Create RBAC resources for the controller |
| `serviceAccount.create` | `true` | Create a ServiceAccount for the controller |

## Usage

Upgrade an existing release after editing `values.yaml`:

```bash
helm upgrade jenkins jenkins/jenkins \
  --namespace jenkins \
  -f jenkins/helm/values.yaml
```

Uninstall:

```bash
helm uninstall jenkins --namespace jenkins
```

Check release status:

```bash
helm status jenkins -n jenkins
```

## Project Structure

```
helm/
  values.yaml    # Helm values overrides for the Jenkins chart
  README.md      # This file
```

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| Pod stuck in `Pending` | PVC cannot be provisioned; storage class missing or full | Run `kubectl describe pvc -n jenkins` and verify the `storageClass` exists |
| LoadBalancer IP not assigned | `loadBalancerIP` conflicts or no LB controller installed | Remove `loadBalancerIP` from values or install MetalLB / cloud LB controller |
| `OOMKilled` on controller pod | Memory limit too low for installed plugins | Increase `controller.resources.limits.memory` in `values.yaml` and run `helm upgrade` |
| Cannot reach Jenkins UI | Firewall blocking the LoadBalancer port | Verify `kubectl get svc -n jenkins` shows an external IP and that port 8080 is reachable |
| Plugins fail to install on startup | Network restrictions or proxy not configured | Set `controller.proxy` values in `values.yaml` or pre-bake plugins into a custom controller image |
