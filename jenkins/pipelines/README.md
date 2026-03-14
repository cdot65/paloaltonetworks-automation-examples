# PAN-OS Automation Pipelines

## Overview

Groovy pipeline scripts for Jenkins that automate Palo Alto Networks PAN-OS configuration via Panorama. Each pipeline spawns a multi-container Kubernetes pod (using the Jenkins Kubernetes plugin), clones this repository, and executes a Python script inside a `pan-os-docker` container to apply the requested configuration.

These pipelines depend on:
- The custom agent image built from `../docker/` (used as the `jnlp` container)
- The RBAC resources from `../manifests/` (the `jenkins-agent-sa` service account)
- A running Jenkins controller deployed via `../helm/`

## Security Warning -- Hardcoded Credentials

**The pipeline scripts contain hardcoded demo credentials that must not be used in production.**

The following default values appear in the source:

- `USERNAME` default: `officehours`
- `PASSWORD` default: `paloalto123`

These exist solely for demonstration purposes. In any non-demo environment, replace the `parameters` block credential handling with Jenkins Credentials binding:

```groovy
// Remove the USERNAME and PASSWORD parameters, then wrap your stages:
withCredentials([usernamePassword(
    credentialsId: 'panorama-credentials',
    usernameVariable: 'USERNAME',
    passwordVariable: 'PASSWORD'
)]) {
    sh '''
        python3 app.py \
            --hostname "$HOSTNAME" \
            --username "$USERNAME" \
            --password "$PASSWORD" \
            ...
    '''
}
```

To set this up:
1. In Jenkins, go to Manage Jenkins > Credentials > System > Global credentials.
2. Add a new "Username with password" credential with ID `panorama-credentials`.
3. Update the pipeline scripts to use `withCredentials` as shown above.

## Prerequisites

- Jenkins controller with the following plugins:
  - [Kubernetes Plugin](https://plugins.jenkins.io/kubernetes/)
  - [Pipeline Utility Steps Plugin](https://plugins.jenkins.io/pipeline-utility-steps/) (for `readJSON`)
- RBAC manifests applied (`../manifests/`)
- Container images available:
  - `ghcr.io/cdot65/jenkins-kubectl:latest` (built from `../docker/`)
  - `ghcr.io/cdot65/pan-os-docker:python`
- Network connectivity from the Kubernetes cluster to the Panorama appliance

## Quickstart

1. In Jenkins, create a new Pipeline job.
2. Under "Pipeline", select "Pipeline script" and paste the contents of one of the `.groovy` files.
3. Save the job and click "Build with Parameters".
4. Fill in the required parameters and run.
5. Check the console output for the JSON result from the Python script.

## Configuration

### address_objects.groovy -- Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `HOSTNAME` | string | `panorama.example.com` | Panorama hostname or IP |
| `USERNAME` | string | `officehours` | **Demo only.** Use Jenkins Credentials in production |
| `PASSWORD` | password | `paloalto123` | **Demo only.** Use Jenkins Credentials in production |
| `DEVICE_GROUP` | string | (empty) | Panorama device group name |
| `ADDRESS_NAME` | string | (empty) | Name for the address object |
| `ADDRESS_TYPE` | string | (empty) | Type (e.g., `ip-netmask`, `ip-range`, `fqdn`) |
| `ADDRESS_TAGS` | string | (empty) | Space-separated tags |
| `ADDRESS_VALUE` | string | (empty) | Address value (IP, range, or FQDN) |
| `ADDRESS_DESCRIPTION` | string | (empty) | Description of the address object |

### security_policy.groovy -- Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `HOSTNAME` | string | `panorama.example.com` | Panorama hostname or IP |
| `USERNAME` | string | `officehours` | **Demo only.** Use Jenkins Credentials in production |
| `PASSWORD` | password | `paloalto123` | **Demo only.** Use Jenkins Credentials in production |
| `DEVICE_GROUP` | choice | `shared` | One of: `shared`, `Magnolia-Proxmox`, `Magnolia-Edge`, `Dallas` |
| `SEC_RULE_NAME` | string | (empty) | Security rule name |
| `SEC_RULE_DESCRIPTION` | string | (empty) | Rule description |
| `SEC_RULE_TAG` | string | `Jenkins` | Space-separated tags |
| `SEC_RULE_DISABLED` | boolean | `false` | Whether to create the rule in disabled state |
| `SEC_RULE_FROM_ZONE` | string | `any` | Source zone(s), space-separated |
| `SEC_RULE_TO_ZONE` | string | `any` | Destination zone(s), space-separated |
| `SEC_RULE_SOURCE` | string | `any` | Source addresses, space-separated |
| `SEC_RULE_DESTINATION` | string | `any` | Destination addresses, space-separated |
| `SEC_RULE_APPLICATION` | string | `any` | App-ID(s), space-separated |
| `SEC_RULE_SERVICE` | string | `any` | TCP/UDP services, space-separated |
| `SEC_RULE_CATEGORY` | string | `any` | URL categories, space-separated |
| `SEC_RULE_SECURITY_PROFILE_GROUP` | string | (empty) | Security profile group |
| `SEC_RULE_LOG_SETTING` | string | (empty) | Log forwarding profile |
| `SEC_RULE_ACTION` | choice | `allow` | One of: `allow`, `deny`, `drop`, `reset-both`, `reset-client`, `reset-server` |

### Pod Template (embedded in both scripts)

Both pipelines define an inline pod template with two containers:

| Container | Image | Purpose |
|---|---|---|
| `jnlp` | `ghcr.io/cdot65/jenkins-kubectl:latest` | Jenkins agent communication + git clone |
| `python` | `ghcr.io/cdot65/pan-os-docker:python` | Runs the PAN-OS Python automation script |

Both containers share a workspace via an `emptyDir` volume mounted at `/home/jenkins/agent`.

## Usage

### From Jenkins UI

1. Open the pipeline job.
2. Click "Build with Parameters".
3. Fill in all fields and click "Build".
4. Monitor the build via Console Output.

Expected successful output (final lines):

```
Script Output: {rule_name=..., status=success, ...}
Finished: SUCCESS
```

### Pipeline Stages

Both pipelines follow the same two-stage pattern:

1. **Setup Workspace** -- Clones `paloaltonetworks-automation-examples` from GitHub inside the `jnlp` container.
2. **Run Python Script** -- Executes the appropriate `app.py` inside the `python` container, captures JSON output, and parses it with `readJSON`.

## Project Structure

```
pipelines/
  address_objects.groovy    # Pipeline to create/update PAN-OS address objects via Panorama
  security_policy.groovy    # Pipeline to create/update PAN-OS security policy rules via Panorama
  README.md                 # This file
```

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| `Failed to parse JSON output` | Python script returned non-JSON output or errored | Check console output for Python tracebacks; verify Panorama connectivity and credentials |
| `git clone` fails in Setup Workspace | Network policy blocking egress or DNS not resolving | Verify the agent pod can reach `github.com`; check cluster DNS |
| `ImagePullBackOff` on `python` container | `ghcr.io/cdot65/pan-os-docker:python` not accessible | Verify image exists and the cluster can pull from GHCR (check imagePullSecrets if private) |
| Pipeline hangs at "Waiting for agent" | No matching pod template or RBAC prevents pod creation | Verify Kubernetes cloud config in Jenkins; check `kubectl get events -n jenkins` |
| `ERROR: script returned exit code 1` | Python script failed (bad credentials, unreachable host, invalid params) | Review the Python error in console output; verify `HOSTNAME` is reachable and credentials are correct |
| Parameters not showing on first run | Jenkins has not yet parsed the `parameters` block | Run the job once (it will fail); subsequent runs will show the parameter form |
