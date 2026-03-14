# Jenkins RBAC Manifests

## Overview

Kubernetes manifests that establish the identity and permissions for Jenkins agent pods. These resources allow dynamically spawned agent pods to interact with the Kubernetes API (e.g., creating pods, listing deployments) as required by the Jenkins Kubernetes plugin and any pipeline steps that call `kubectl`.

This component works alongside the Helm deployment (`../helm/`) which handles the controller's own ServiceAccount. The manifests here are specifically for the **agent** service account referenced by the pod templates in `../pipelines/`.

## Prerequisites

- `kubectl` configured with cluster-admin or equivalent access
- The `jenkins` namespace must exist (created by `helm install --create-namespace` or manually)

## Quickstart

1. Apply all manifests:

   ```bash
   kubectl apply -f jenkins/manifests/
   ```

2. Verify the resources:

   ```bash
   kubectl get serviceaccount jenkins-agent-sa -n jenkins
   kubectl get clusterrole jenkins-agent-role
   kubectl get clusterrolebinding jenkins-agent-binding
   ```

3. Confirm the binding links the correct SA and role:

   ```bash
   kubectl describe clusterrolebinding jenkins-agent-binding
   ```

## Configuration

### service-account.yaml

| Field | Value | Notes |
|---|---|---|
| `metadata.name` | `jenkins-agent-sa` | Referenced by pod templates in pipeline scripts and `jenkins-agent-pod-template.yaml` |
| `metadata.namespace` | `jenkins` | Must match the namespace where agent pods run |

### cluster-role.yaml

| Field | Value | Notes |
|---|---|---|
| `metadata.name` | `jenkins-agent-role` | Cluster-scoped role |
| `rules[0].apiGroups` | `""`, `apps`, `batch` | Core, apps, and batch API groups |
| `rules[0].resources` | `pods`, `pods/log`, `deployments`, `jobs`, `namespaces` | Resources agents can access |
| `rules[0].verbs` | `get`, `list`, `watch`, `create`, `delete`, `patch` | Allowed operations |

To restrict agents to a single namespace, convert the `ClusterRole` / `ClusterRoleBinding` to a namespaced `Role` / `RoleBinding`.

### cluster-role-binding.yaml

| Field | Value | Notes |
|---|---|---|
| `subjects[0].name` | `jenkins-agent-sa` | Must match the ServiceAccount name |
| `subjects[0].namespace` | `jenkins` | Must match the ServiceAccount namespace |
| `roleRef.name` | `jenkins-agent-role` | Must match the ClusterRole name |

### jenkins-agent-pod-template.yaml

Reference pod spec for configuring the Jenkins Kubernetes plugin via the UI (as opposed to inline YAML in pipeline scripts).

| Field | Value | Notes |
|---|---|---|
| `spec.serviceAccountName` | `jenkins-agent-sa` | Links the pod to the RBAC chain |
| `containers[0].image` | `jenkins/inbound-agent:latest` | Base image; replace with custom image from `../docker/` if kubectl is needed |
| `resources.requests.cpu` | `500m` | Adjust per workload |
| `resources.requests.memory` | `512Mi` | Adjust per workload |
| `resources.limits.cpu` | `1` | Adjust per workload |
| `resources.limits.memory` | `1024Mi` | Adjust per workload |
| `volumes[0]` | `emptyDir: {}` | Ephemeral workspace; data lost when pod terminates |

## Usage

Delete and recreate all manifests (e.g., after editing):

```bash
kubectl delete -f jenkins/manifests/
kubectl apply -f jenkins/manifests/
```

Test that the service account can list pods:

```bash
kubectl auth can-i list pods --as=system:serviceaccount:jenkins:jenkins-agent-sa
```

Expected output: `yes`

## Project Structure

```
manifests/
  service-account.yaml              # ServiceAccount for Jenkins agent pods
  cluster-role.yaml                 # ClusterRole granting pod/deployment/job access
  cluster-role-binding.yaml         # Binds the ClusterRole to the ServiceAccount
  jenkins-agent-pod-template.yaml   # Reference pod template for the Kubernetes plugin UI
  README.md                         # This file
```

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| Agent pod fails with `Forbidden` errors | ServiceAccount not bound to ClusterRole, or namespace mismatch | Verify `kubectl describe clusterrolebinding jenkins-agent-binding` shows the correct SA and namespace |
| `serviceaccount "jenkins-agent-sa" not found` | Manifests not applied, or applied to wrong namespace | Run `kubectl apply -f jenkins/manifests/` and confirm the namespace is `jenkins` |
| Agent cannot create pods in other namespaces | ClusterRole does not include the target namespace's resources | This is expected with a namespaced Role; use ClusterRole/ClusterRoleBinding for cross-namespace access |
| Pod template not appearing in Jenkins UI | Template YAML not pasted into Kubernetes cloud config | Copy `jenkins-agent-pod-template.yaml` content into Manage Jenkins > Clouds > Pod Templates |
| Agent pod evicted or OOMKilled | Resource limits in the pod template too low | Increase `resources.limits.memory` in the pod template or pipeline YAML |
