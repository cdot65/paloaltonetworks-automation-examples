# Jenkins on Kubernetes: Dynamic Workload Instantiation Guide

Welcome to this comprehensive guide on deploying Jenkins on Kubernetes with dynamic workload instantiation. This guide
is designed to help you set up Jenkins in a Kubernetes cluster, configure it for dynamic agents, and run pipelines that
execute tasks within the cluster. Whether you're new to Jenkins or Kubernetes, this guide will walk you through each
step with detailed explanations.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
    - [Deploy Jenkins using Helm](#deploy-jenkins-using-helm)
    - [Configure Service Account and RBAC](#configure-service-account-and-rbac)
- [Configuring Jenkins for Dynamic Workloads](#configuring-jenkins-for-dynamic-workloads)
    - [Step 1: Build a Custom Jenkins Agent Image](#step-1-build-a-custom-jenkins-agent-image)
    - [Step 2: Configure the Kubernetes Plugin in Jenkins](#step-2-configure-the-kubernetes-plugin-in-jenkins)
    - [Step 3: Create a Jenkins Pipeline](#step-3-create-a-jenkins-pipeline)
    - [Step 4: Implement Best Practices and Security Measures](#step-4-implement-best-practices-and-security-measures)
- [Understanding the Pipeline Script](#understanding-the-pipeline-script)
- [Detailed Explanation of Components](#detailed-explanation-of-components)
    - [Jenkins Pipeline Script](#jenkins-pipeline-script)
    - [Python Scripts](#python-scripts)
    - [Dockerfile](#dockerfile)
    - [Helm Values File](#helm-values-file)
    - [Kubernetes Manifests](#kubernetes-manifests)
- [Additional Considerations](#additional-considerations)
- [Conclusion](#conclusion)
- [Resources](#resources)

---

## Introduction

Jenkins is a popular automation server used for continuous integration and continuous delivery (CI/CD). Running Jenkins
on Kubernetes allows you to leverage the scalability and resilience of Kubernetes while managing your CI/CD workflows.

In this guide, we'll deploy Jenkins on a Kubernetes cluster using Helm, configure it to use dynamic agents that run as
Kubernetes pods, and set up a pipeline that executes a Python script. This pipeline will interact with Palo Alto
Networks Panorama to configure security policies.

---

## Prerequisites

Before you begin, ensure you have the following:

- **Kubernetes Cluster**: A running Kubernetes cluster with `kubectl` access.
- **Helm**: The Helm package manager installed on your local machine.
- **Docker**: Docker installed locally to build and push custom images.
- **Docker Registry**: Access to a Docker registry (e.g., Docker Hub) to push custom images.
- **Git**: Git installed locally to clone repositories.
- **Jenkins Plugins**: Jenkins should have the following plugins installed:
    - [Kubernetes Plugin](https://plugins.jenkins.io/kubernetes/)
    - [Pipeline Utility Steps Plugin](https://plugins.jenkins.io/pipeline-utility-steps/)
- **Basic Knowledge**: Familiarity with Kubernetes and Jenkins is helpful but not required.

---

## Installation

### Deploy Jenkins using Helm

Helm is a package manager for Kubernetes that simplifies deployment of complex applications. We'll use the official
Jenkins Helm chart to deploy Jenkins.

#### Step 1: Add Jenkins Helm Repository

First, add the Jenkins Helm repository and update your local Helm repositories.

```bash
helm repo add jenkins https://charts.jenkins.io
helm repo update
```

#### Step 2: Create `values.yaml`

Customize your Jenkins installation by creating a `values.yaml` file. This file allows you to override default settings
provided by the Helm chart. Here's an example `values.yaml`:

```yaml
controller:
  serviceType: LoadBalancer
  loadBalancerIP: <YOUR_LOAD_BALANCER_IP>  # Replace with your desired IP
  ingress:
    enabled: false
  resources:
    requests:
      cpu: "500m"
      memory: "1024Mi"
    limits:
      cpu: "2000m"
      memory: "4096Mi"

persistence:
  enabled: true
  storageClass: "local-path"  # Use your cluster's default storage class
  size: "20Gi"

rbac:
  create: true

serviceAccount:
  create: true
```

**Note:** Replace `<YOUR_LOAD_BALANCER_IP>` with the IP address you want to assign to the Jenkins service, or omit this
line to let Kubernetes assign one automatically.

#### Step 3: Install Jenkins

Install Jenkins into a namespace called `jenkins`.

```bash
helm install jenkins jenkins/jenkins --namespace jenkins -f values.yaml --create-namespace
```

#### Step 4: Monitor Jenkins Deployment

Check the status of the Jenkins service and pods.

```bash
kubectl get svc -n jenkins
kubectl get pods -n jenkins
```

#### Step 5: Retrieve Jenkins Admin Password

Get the initial admin password to log into Jenkins.

```bash
kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/additional/chart-admin-password && echo
```

Use this password to log into Jenkins at `http://<YOUR_LOAD_BALANCER_IP>:8080`.

---

### Configure Service Account and RBAC

To allow Jenkins agents to interact with the Kubernetes cluster, we need to set up appropriate permissions.

#### Step 1: Create a Service Account

Create a `ServiceAccount` that Jenkins agents will use.

```yaml
# service-account.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: jenkins-agent-sa
  namespace: jenkins
```

#### Step 2: Define a ClusterRole

Define a `ClusterRole` that specifies the permissions needed.

```yaml
# cluster-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: jenkins-agent-role
rules:
  - apiGroups: [ "", "apps", "batch" ]
    resources: [ "pods", "pods/log", "deployments", "jobs", "namespaces" ]
    verbs: [ "get", "list", "watch", "create", "delete", "patch" ]
```

#### Step 3: Bind the ClusterRole to the Service Account

Bind the `ClusterRole` to the `ServiceAccount` using a `ClusterRoleBinding`.

```yaml
# cluster-role-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: jenkins-agent-binding
subjects:
  - kind: ServiceAccount
    name: jenkins-agent-sa
    namespace: jenkins
roleRef:
  kind: ClusterRole
  name: jenkins-agent-role
  apiGroup: rbac.authorization.k8s.io
```

#### Step 4: Apply the Configurations

Apply the configurations to your cluster.

```bash
kubectl apply -f service-account.yaml
kubectl apply -f cluster-role.yaml
kubectl apply -f cluster-role-binding.yaml
```

---

## Configuring Jenkins for Dynamic Workloads

Now that Jenkins is installed and the necessary Kubernetes permissions are set up, we can configure Jenkins to use
dynamic agents running as Kubernetes pods.

### Step 1: Build a Custom Jenkins Agent Image

We'll build a custom Jenkins agent Docker image that includes necessary tools like `kubectl`.

#### Dockerfile

Create a `Dockerfile` with the following content:

```Dockerfile
FROM jenkins/inbound-agent:latest

USER root

# Install dependencies
RUN apt-get update && \
    apt-get install -y apt-transport-https gnupg2 curl ca-certificates && \
    curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add - && \
    apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && mv kubectl /usr/local/bin/

USER jenkins
```

#### Build and Push the Image

Build the Docker image and push it to your Docker registry.

```bash
docker build -t <yourregistry>/jenkins-agent-kubectl:latest .
docker push <yourregistry>/jenkins-agent-kubectl:latest
```

**Note:** Replace `<yourregistry>` with your Docker registry name.

### Step 2: Configure the Kubernetes Plugin in Jenkins

#### Access Jenkins Dashboard

Navigate to your Jenkins instance (e.g., `http://<YOUR_LOAD_BALANCER_IP>:8080`).

#### Configure Kubernetes Cloud

1. Go to **Manage Jenkins** > **Manage Nodes and Clouds** > **Configure Clouds**.
2. Add a new Kubernetes cloud configuration or edit the existing one.
3. Ensure Jenkins can connect to your Kubernetes cluster. Use the Kubernetes service account token and API server URL if
   necessary.

#### Configure Pod Templates

1. In the Kubernetes cloud configuration, scroll to **Pod Templates**.
2. Add a new Pod Template with the following settings:
    - **Name:** `jenkins-agent`
    - **Labels:** `dynamic-agent`
    - **Namespace:** `jenkins`
    - **Service Account:** `jenkins-agent-sa`
3. Under **Containers**, add:
    - **Name:** `jnlp`
    - **Docker Image:** `<yourregistry>/jenkins-agent-kubectl:latest`
    - **Working Directory:** `/home/jenkins/agent`
4. Add an **Empty Dir Volume** with a mount path of `/home/jenkins/agent`.

### Step 3: Create a Jenkins Pipeline

We'll create a Jenkins pipeline that clones a repository and runs a Python script within a dynamically created
Kubernetes pod.

#### Pipeline Script

In Jenkins, create a new **Pipeline** job and use the following pipeline script:

```groovy
pipeline {
    agent {
        kubernetes {
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: jenkins-agent
spec:
  serviceAccountName: jenkins-agent-sa
  containers:
    - name: jnlp
      image: <yourregistry>/jenkins-agent-kubectl:latest
      resources:
        requests:
          cpu: "500m"
          memory: "512Mi"
        limits:
          cpu: "1"
          memory: "1024Mi"
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent
    - name: python
      image: ghcr.io/cdot65/pan-os-docker:python
      imagePullPolicy: Always
      command:
        - cat
      tty: true
      workingDir: /home/jenkins/agent
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent
  volumes:
    - name: workspace-volume
      emptyDir: {}
"""
        }
    }
    parameters {
        string(name: 'HOSTNAME', defaultValue: 'panorama1.example.com', description: 'Panorama hostname')
        string(name: 'USERNAME', defaultValue: 'admin', description: 'Panorama username')
        password(name: 'PASSWORD', defaultValue: '', description: 'Panorama password')
        choice(name: 'DEVICE_GROUP', choices: ['shared', 'Group1', 'Group2'], description: 'Panorama device group')
        string(name: 'SEC_RULE_NAME', defaultValue: '', description: 'Name of the security rule')
        string(name: 'SEC_RULE_DESCRIPTION', defaultValue: '', description: 'Description of the security rule')
        string(name: 'SEC_RULE_TAG', defaultValue: '', description: 'Tags, space-separated list')
        booleanParam(name: 'SEC_RULE_DISABLED', defaultValue: false, description: 'Set the policy as disabled')
        string(name: 'SEC_RULE_FROM_ZONE', defaultValue: 'any', description: 'Source security zone(s), space-separated list')
        string(name: 'SEC_RULE_TO_ZONE', defaultValue: 'any', description: 'Destination security zone(s), space-separated list')
        string(name: 'SEC_RULE_SOURCE', defaultValue: 'any', description: 'Source addresses, space-separated list')
        string(name: 'SEC_RULE_DESTINATION', defaultValue: 'any', description: 'Destination addresses, space-separated list')
        string(name: 'SEC_RULE_APPLICATION', defaultValue: 'any', description: 'App-ID, space-separated list')
        string(name: 'SEC_RULE_SERVICE', defaultValue: 'any', description: 'TCP/UDP services, space-separated list')
        string(name: 'SEC_RULE_CATEGORY', defaultValue: 'any', description: 'URL Categories, space-separated list')
        string(name: 'SEC_RULE_SECURITY_PROFILE_GROUP', defaultValue: '', description: 'Security profile group associated to rule')
        string(name: 'SEC_RULE_LOG_SETTING', defaultValue: '', description: 'Log forwarding profile')
        choice(name: 'SEC_RULE_ACTION', choices: ['allow', 'deny', 'drop', 'reset-both', 'reset-client', 'reset-server'], description: 'Action for the rule')
    }
    stages {
        stage('Setup Workspace') {
            steps {
                container('jnlp') {
                    sh '''
                        git clone https://github.com/your-repo/paloaltonetworks-automation-examples.git
                    '''
                }
            }
        }
        stage('Run Python Script') {
            steps {
                container('python') {
                    script {
                        def ruleDisabledFlag = SEC_RULE_DISABLED ? '--rule-disabled' : ''
                        sh '''
                            cd paloaltonetworks-automation-examples/python/pan-os-configure-security-policies

                            set -e
                            python3 app.py \
                                --hostname "$HOSTNAME" \
                                --username "$USERNAME" \
                                --password "$PASSWORD" \
                                --device-group "$DEVICE_GROUP" \
                                --rule-name "$SEC_RULE_NAME" \
                                --rule-description "$SEC_RULE_DESCRIPTION" \
                                --rule-tag $SEC_RULE_TAG \
                                ${ruleDisabledFlag} \
                                --rule-from-zone $SEC_RULE_FROM_ZONE \
                                --rule-to-zone $SEC_RULE_TO_ZONE \
                                --rule-source $SEC_RULE_SOURCE \
                                --rule-destination $SEC_RULE_DESTINATION \
                                --rule-application $SEC_RULE_APPLICATION \
                                --rule-service $SEC_RULE_SERVICE \
                                --rule-category $SEC_RULE_CATEGORY \
                                --rule-security-profile-group "$SEC_RULE_SECURITY_PROFILE_GROUP" \
                                --rule-log-setting "$SEC_RULE_LOG_SETTING" \
                                --rule-action "$SEC_RULE_ACTION" > output.json
                        '''

                        try {
                            def jsonOutput = readFile('paloaltonetworks-automation-examples/python/pan-os-configure-security-policies/output.json').trim()
                            def json = readJSON text: jsonOutput
                            echo "Script Output: ${json}"
                        } catch (Exception e) {
                            echo "Failed to parse JSON output: ${e}"
                            currentBuild.result = 'FAILURE'
                            error("Pipeline aborted due to JSON parsing error.")
                        }
                    }
                }
            }
        }
    }
}
```

**Note:** Replace `<yourregistry>` and the Git repository URL with your own values.

### Step 4: Implement Best Practices and Security Measures

#### Namespaces for Isolation

While not explicitly defined in the pipeline, it's a good practice to run builds in isolated namespaces if your
pipelines create Kubernetes resources.

#### RBAC Policies

Ensure that the `ClusterRole` and `ClusterRoleBinding` only grant the minimum required permissions to Jenkins agents.

#### Secrets Management

- Use Jenkins Credentials to securely store sensitive information like passwords.
- Replace the `PASSWORD` parameter with a credentials binding in Jenkins.
- **Example**: Create a Jenkins credential with ID `PANORAMA_PASSWORD` and use it in your pipeline.
  ```groovy
  withCredentials([usernamePassword(credentialsId: 'PANORAMA_CREDENTIALS', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
      // Your script here
  }
  ```
- Update your pipeline to use these credentials.

#### Resource Quotas

Implement resource quotas to prevent resource exhaustion.

```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: jenkins-pipeline-quota
  namespace: jenkins
spec:
  hard:
    pods: "20"
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
```

Apply the resource quota:

```bash
kubectl apply -f resource-quota.yaml
```

---

## Understanding the Pipeline Script

Let's break down the pipeline script to understand how it works.

### Agent Configuration

- **Kubernetes Agent**: The pipeline runs on a Kubernetes agent defined in the `agent` block.
- **Pod Template**: A custom pod is defined using YAML, which includes two containers:
    - **`jnlp` Container**: The Jenkins agent container that handles communication with the Jenkins master.
    - **`python` Container**: Runs the Python script.

### Parameters

The pipeline defines several parameters required to configure the security rule in Panorama.

- **Credential Parameters**:
    - `PASSWORD`: Should be handled securely using Jenkins Credentials.
- **String Parameters**:
    - `HOSTNAME`, `USERNAME`, `SEC_RULE_NAME`, etc.
- **Choice Parameters**:
    - `DEVICE_GROUP`, `SEC_RULE_ACTION`.
- **Boolean Parameters**:
    - `SEC_RULE_DISABLED`.

### Stages

#### Stage: Setup Workspace

- **Purpose**: Clones the Git repository containing the Python scripts.
- **Container**: Runs in the `jnlp` container where Git is available.

#### Stage: Run Python Script

- **Purpose**: Executes the Python script with the provided parameters.
- **Container**: Runs in the `python` container where Python and dependencies are available.
- **Script Execution**:
    - Constructs the command to run `app.py` with appropriate arguments.
    - Handles optional parameters and flags.
- **Error Handling**:
    - Tries to read and parse the output JSON.
    - If parsing fails, marks the build as failed.

---

## Detailed Explanation of Components

### Jenkins Pipeline Script

The pipeline script is written in Groovy and defines the CI/CD workflow. Key components include:

- **Agent Definition**: Specifies that the pipeline runs on a Kubernetes agent.
- **Parameters**: Collects user input necessary for the pipeline.
- **Stages**: Breaks down the pipeline into logical steps.
- **Containers**: Specifies the containers to use within the agent pod.
- **Error Handling**: Includes try-catch blocks to manage exceptions.

### Python Scripts

#### `app.py`

This script connects to Palo Alto Networks Panorama and configures security policies based on the provided arguments.

- **Argument Parsing**: Uses `argparse` to handle command-line arguments.
- **Connection Handling**: Establishes a connection to Panorama using provided credentials.
- **Configuration Management**: Prepares the security rule configuration and applies it.
- **Commit Changes**: Commits and pushes changes to the device group.
- **Error Handling**: Logs errors and returns appropriate exit codes.

#### `paloconfig.py`

A helper module that contains the `PaloConfig` class, which provides methods to interact with Panorama.

- **Methods Include**:
    - `commit_panorama`: Commits changes to Panorama.
    - `commit_all`: Commits changes to all devices in a device group.
    - `create_device_group`: Creates or retrieves a device group.
    - `security_rules`: Configures security rules.

### Dockerfile

Defines a custom Jenkins agent image that includes `kubectl`.

- **Base Image**: `jenkins/inbound-agent:latest`.
- **Installations**:
    - Installs `kubectl` to interact with Kubernetes.
    - Includes any other required dependencies.

### Helm Values File

Configures the Jenkins Helm chart deployment.

- **Service Type**: `LoadBalancer` to expose Jenkins externally.
- **Resource Allocation**: Sets resource requests and limits.
- **Persistence**: Enables persistence for Jenkins data.
- **RBAC**: Ensures RBAC resources are created.

### Kubernetes Manifests

Defines resources required for Jenkins agents to function correctly.

- **Service Account**: `jenkins-agent-sa` for agents.
- **ClusterRole**: `jenkins-agent-role` with necessary permissions.
- **ClusterRoleBinding**: Binds the role to the service account.
- **Resource Quota**: Limits resource usage in the namespace.

---

## Additional Considerations

- **Plugin Dependencies**: Ensure required Jenkins plugins are installed.
- **Security**:
    - Use Jenkins Credentials for sensitive data.
    - Limit permissions with RBAC.
- **Container Requirements**:
    - Verify that containers have all necessary dependencies.
- **Error Handling**:
    - Implement robust error handling in scripts and pipelines.
- **Documentation**:
    - Comment your code and scripts for maintainability.

---

## Conclusion

By following this guide, you have:

- Deployed Jenkins on Kubernetes using Helm.
- Configured Jenkins to use dynamic agents running as Kubernetes pods.
- Created a pipeline that automates the configuration of security policies in Panorama.
- Implemented best practices for security, resource management, and error handling.

This setup allows you to leverage Kubernetes' scalability and Jenkins' automation capabilities to enhance your CI/CD
workflows.

---

## Resources

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Helm Documentation](https://helm.sh/docs/)
- [Palo Alto Networks PAN-OS SDK for Python](https://github.com/PaloAltoNetworks/pan-os-python)
- [Docker Documentation](https://docs.docker.com/)

---

**Feel free to customize and extend this setup to suit your specific needs. Happy automating!**

---