# Jenkins on Kubernetes with Dynamic Workload Instantiation

This repository provides step-by-step instructions to deploy Jenkins on Kubernetes using Helm and configure it for dynamic workload instantiation. The Jenkins setup is enhanced to execute pipelines that spawn workloads within the Kubernetes cluster dynamically.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Deploy Jenkins using Helm](#deploy-jenkins-using-helm)
  - [Configure Service Account and RBAC](#configure-service-account-and-rbac)
- [Configuring Jenkins for Dynamic Workloads](#configuring-jenkins-for-dynamic-workloads)
  - [Step 1: Create a Jenkins Agent Configuration](#step-1-create-a-jenkins-agent-configuration)
  - [Step 2: Set Up the Kubernetes Plugin in Jenkins](#step-2-set-up-the-kubernetes-plugin-in-jenkins)
  - [Step 3: Create a Jenkins Pipeline](#step-3-create-a-jenkins-pipeline)
  - [Step 4: Implement Best Practices and Security Considerations](#step-4-implement-best-practices-and-security-considerations)
- [Pipeline Script Explanation](#pipeline-script-explanation)
- [Additional Considerations](#additional-considerations)
- [Conclusion](#conclusion)

---

## Prerequisites

- **Kubernetes Cluster**: A running Kubernetes cluster with `kubectl` access.
- **Helm**: Helm package manager installed locally.
- **Docker Registry**: Access to a Docker registry to push custom images.
- **Git**: Git installed locally to clone repositories.
- **Jenkins Plugins**: Jenkins should have the following plugins installed:
  - Kubernetes Plugin
  - Pipeline Utility Steps Plugin

---

## Installation

### Deploy Jenkins using Helm

1. **Add Jenkins Helm Repository:**

   ```bash
   helm repo add jenkins https://charts.jenkins.io
   helm repo update
   ```

2. **Create `values.yaml` (Optional):**

   Customize Jenkins installation by creating a `values.yaml` file. This can include custom configurations like persistence, service type, ingress, etc.

3. **Install Jenkins:**

   ```bash
   helm install jenkins jenkins/jenkins --namespace jenkins -f values.yaml --create-namespace
   ```

4. **Monitor the Jenkins Service:**

   ```bash
   kubectl get svc -n jenkins -w jenkins
   ```

5. **Check Jenkins Pods:**

   ```bash
   kubectl get pods -n jenkins
   ```

6. **Retrieve Jenkins Admin Password:**

   ```bash
   kubectl exec --namespace jenkins -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/additional/chart-admin-password && echo
   ```

### Configure Service Account and RBAC

1. **Create a Service Account for Jenkins Agents:**

   ```yaml
   # service-account.yaml
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: jenkins-agent-sa
     namespace: jenkins
   ```

2. **Define ClusterRole with Necessary Permissions:**

   ```yaml
   # cluster-role.yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRole
   metadata:
     name: jenkins-agent-role
   rules:
     - apiGroups: ["", "apps", "batch"]
       resources: ["pods", "pods/log", "deployments", "jobs", "namespaces"]
       verbs: ["get", "list", "watch", "create", "delete", "patch"]
   ```

3. **Bind the ClusterRole to the Service Account:**

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

4. **Apply the Configurations:**

   ```bash
   kubectl apply -f service-account.yaml
   kubectl apply -f cluster-role.yaml
   kubectl apply -f cluster-role-binding.yaml
   ```

---

## Configuring Jenkins for Dynamic Workloads

### Step 1: Create a Jenkins Agent Configuration

#### 1. Build a Custom Jenkins Agent Docker Image

**Dockerfile:**

```Dockerfile
FROM jenkins/inbound-agent:latest

USER root

# Install kubectl and git
RUN apt-get update && \
    apt-get install -y apt-transport-https gnupg2 curl ca-certificates git && \
    curl -fsSL https://apt.kubernetes.io/doc/apt-key.gpg | apt-key add - && \
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list && \
    apt-get update && \
    apt-get install -y kubectl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jenkins
```

**Build and Push the Image:**

```bash
docker build -t yourregistry/jenkins-agent-kubectl:latest .
docker push yourregistry/jenkins-agent-kubectl:latest
```

*Replace `yourregistry` with your Docker registry (e.g., Docker Hub username).*

### Step 2: Set Up the Kubernetes Plugin in Jenkins

1. **Access Jenkins Dashboard:**

   Navigate to your Jenkins URL (e.g., `http://your-jenkins-url`).

2. **Configure Kubernetes Cloud:**

   - Go to `Manage Jenkins` > `Manage Nodes and Clouds` > `Configure Clouds`.
   - Use the existing Kubernetes cloud configuration or add a new one if necessary.
   - Ensure Jenkins can communicate with the Kubernetes cluster (Test Connection should succeed).

3. **Configure Pod Templates:**

   - In the Kubernetes Cloud configuration, scroll to **Pod Templates**.
   - Add a new Pod Template or modify the existing one.
     - **Name:** `jenkins-agent`
     - **Labels:** `dynamic-agent`
     - **Containers:**
       - **Name:** `jnlp`
       - **Docker Image:** `yourregistry/jenkins-agent-kubectl:latest`
     - **Volumes:**
       - Add an **Empty Dir Volume** with a mount path of `/home/jenkins/agent`.

### Step 3: Create a Jenkins Pipeline

Create a Jenkins pipeline that can spawn workloads and execute a Python script from a public repository.

**Jenkinsfile:**

```groovy
pipeline {
    agent {
        kubernetes {
            label 'dynamic-agent'
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
      image: yourregistry/jenkins-agent-kubectl:latest
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
        string(name: 'NAME', defaultValue: '', description: 'Name parameter')
        string(name: 'SOURCE_ZONE', defaultValue: '', description: 'Source zone(s), comma-separated')
        string(name: 'DESTINATION_ZONE', defaultValue: '', description: 'Destination zone(s), comma-separated')
        string(name: 'APPLICATION', defaultValue: '', description: 'Application(s), comma-separated')
    }
    environment {
        NAMESPACE = "jenkins-pipeline-${env.BUILD_NUMBER}"
    }
    stages {
        stage('Setup Workspace') {
            steps {
                container('jnlp') {
                    script {
                        sh '''
                            git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
                        '''
                    }
                }
            }
        }
        stage('Run Python Script') {
            steps {
                container('python') {
                    script {
                        sh """
                            cd paloaltonetworks-automation-examples/python/pan-os-global-search

                            NAME_PARAM="--name '${NAME}'"

                            SOURCE_ZONE_PARAMS=""
                            for zone in \$(echo "${SOURCE_ZONE}" | tr ',' '\\n'); do
                                SOURCE_ZONE_PARAMS="\$SOURCE_ZONE_PARAMS --source-zone '\$zone'"
                            done

                            DESTINATION_ZONE_PARAMS=""
                            for zone in \$(echo "${DESTINATION_ZONE}" | tr ',' '\\n'); do
                                DESTINATION_ZONE_PARAMS="\$DESTINATION_ZONE_PARAMS --destination-zone '\$zone'"
                            done

                            APPLICATION_PARAMS=""
                            for app in \$(echo "${APPLICATION}" | tr ',' '\\n'); do
                                APPLICATION_PARAMS="\$APPLICATION_PARAMS --application '\$app'"
                            done

                            python3 app.py \\
                                \$NAME_PARAM \\
                                \$SOURCE_ZONE_PARAMS \\
                                \$DESTINATION_ZONE_PARAMS \\
                                \$APPLICATION_PARAMS > output.json
                        """
                        // Read the output JSON
                        def jsonOutput = readFile('paloaltonetworks-automation-examples/python/pan-os-global-search/output.json').trim()
                        // Parse the JSON
                        def json = readJSON text: jsonOutput
                        // Use the JSON object as needed
                        echo "Script Output: ${json}"
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                // Cleanup resources if applicable
                sh "kubectl delete namespace ${NAMESPACE} || true"
            }
        }
    }
}
```

### Step 4: Implement Best Practices and Security Considerations

1. **Namespaces for Isolation:**

   - Each pipeline run creates a unique Kubernetes namespace for resource isolation.
   - Resources are cleaned up in the `post` section to prevent resource exhaustion.

2. **RBAC Policies:**

   - The `ClusterRole` and `ClusterRoleBinding` restrict Jenkins' permissions to necessary operations.

3. **Secrets Management:**

   - Use Jenkins Credentials Binding plugin and Kubernetes Secrets to handle sensitive information securely.

4. **Resource Quotas:**

   - Implement Kubernetes `ResourceQuota` to limit resource usage per namespace.

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

   **Apply the Resource Quota:**

   ```bash
   kubectl apply -f resource-quota.yaml
   ```

---

## Pipeline Script Explanation

- **Agent Configuration:**

  - Uses a Kubernetes agent with two containers:
    - **`jnlp` Container:**
      - Custom Jenkins agent image with `kubectl` and `git` installed.
      - Handles cloning repositories and interacting with Kubernetes.
    - **`python` Container:**
      - Uses `ghcr.io/cdot65/pan-os-docker:python` image.
      - Executes the Python script.

- **Parameters:**

  - Collects user input for `NAME`, `SOURCE_ZONE`, `DESTINATION_ZONE`, and `APPLICATION`.

- **Environment Variables:**

  - `NAMESPACE` is set to `jenkins-pipeline-${env.BUILD_NUMBER}` for unique namespace creation.

- **Stages:**

  1. **Setup Workspace:**
     - Clones the repository containing the Python script.
  2. **Run Python Script:**
     - Executes the Python script with user-provided parameters.
     - Handles comma-separated values and converts them into script arguments.
     - Captures and parses the JSON output.

- **Post Actions:**

  - Cleans up Kubernetes resources by deleting the namespace created for the pipeline.

---

## Additional Considerations

- **Plugin Dependencies:**

  - Ensure the **Pipeline Utility Steps** plugin is installed for JSON parsing.

- **Script Compatibility:**

  - Verify that the Python script accepts parameters as provided.

- **Security:**

  - Use Jenkins credentials and Kubernetes secrets for any sensitive data required by the Python script.

- **Container Requirements:**

  - Ensure the `python` container has all necessary dependencies for the script.

- **Error Handling:**

  - Implement error handling in the pipeline to manage failures gracefully.

---

## Conclusion

By following the steps outlined in this guide, you have successfully:

- Deployed Jenkins on Kubernetes using Helm.
- Configured Jenkins to use dynamic agents in Kubernetes.
- Created a pipeline that executes a Python script in a containerized environment.
- Implemented best practices for security and resource management.

This setup enhances your CI/CD capabilities by leveraging Kubernetes' scalability and Jenkins' automation features.

---

**Feel free to customize and extend this setup according to your specific requirements.**