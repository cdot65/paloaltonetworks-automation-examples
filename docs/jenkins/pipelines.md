# Jenkins Pipelines

[View on GitHub](https://github.com/cdot65/paloaltonetworks-automation-examples/tree/main/jenkins/pipelines)

Groovy Jenkins pipeline scripts that spawn multi-container Kubernetes agent pods and execute Python scripts against Panorama.

## Available Pipelines

### Address Objects Pipeline

Creates address objects on Panorama by:

1. Spawning a K8s pod with JNLP agent + Python containers
2. Cloning the automation repository
3. Installing Python dependencies
4. Running the address object creation script against Panorama

### Security Policy Pipeline

Creates security policy rules on Panorama following the same pod-based execution pattern.

## Pipeline Structure

Each pipeline defines:

- **Pod template** with two containers (JNLP for Jenkins connectivity, Python for script execution)
- **Parameters** for Panorama hostname, credentials, and configuration options
- **Stages** for checkout, setup, and execution

!!! warning "Credentials"
    Never hardcode credentials in pipeline scripts. Use Jenkins Credentials binding (`withCredentials`) to inject secrets at runtime:
    ```groovy
    withCredentials([usernamePassword(credentialsId: 'panorama-creds',
                     usernameVariable: 'PAN_USER',
                     passwordVariable: 'PAN_PASS')]) {
        sh "python main.py --user ${PAN_USER} --pass ${PAN_PASS}"
    }
    ```
