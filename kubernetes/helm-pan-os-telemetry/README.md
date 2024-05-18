# PAN-OS Telemetry Stack Deployment 📚

This README provides an overview of our container image project and guides you through the setup and execution process. 🚀

## Table of Contents

- [PAN-OS Telemetry Stack Deployment 📚](#pan-os-telemetry-stack-deployment-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Installing a lightweight Kubernetes host with k3s](#installing-a-lightweight-kubernetes-host-with-k3s)
    - [Install Script](#install-script)
  - [Helm Project Structure](#helm-project-structure)
    - [Chart.yaml](#chartyaml)
    - [values.yaml](#valuesyaml)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our container image project aims to automate the creation of a PAN-OS telemetry stack. By leveraging the powerful CLI commands from Helm, we can streamline the process and ensure consistent and reproducible results across multiple environments. 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Kubernetes host
- Helm installed

## Setup

### Installing a lightweight Kubernetes host with k3s

This guide will help you quickly launch a cluster with default options. The installation section covers in greater detail how K3s can be set up.

Make sure your nodes meet the requirements before proceeding.

For information on how K3s components work together, refer to the architecture section.

### Install Script

K3s provides an installation script that is a convenient way to install it as a service on systemd or openrc based systems. This script is available at https://get.k3s.io. To install K3s using this method, just run:

```bash
curl -sfL https://get.k3s.io | sh -
```

After running this installation:

The K3s service will be configured to automatically restart after node reboots or if the process crashes or is killed

Additional utilities will be installed, including kubectl, crictl, ctr, k3s-killall.sh, and k3s-uninstall.sh

A kubeconfig file will be written to /etc/rancher/k3s/k3s.yaml and the kubectl installed by K3s will automatically use it

A single-node server installation is a fully-functional Kubernetes cluster, including all the datastore, control-plane, kubelet, and container runtime components necessary to host workload pods. It is not necessary to add additional server or agents nodes, but you may want to do so to add additional capacity or redundancy to your cluster.

## Helm Project Structure

### Chart.yaml

Our Helm chart (`Chart.yaml`) is structured as follows:

```yaml
apiVersion: v2
name: pan-os-telemetry
description: A Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "1.16.0"
icon: "https://companieslogo.com/img/orig/PANW-4618d203.png?t=1647840523"
```

The `Chart.yaml` file sets up our Helm chart with the following key-value pairs:

- **apiVersion**: Specifies the version of the Helm chart API.
- **name**: The name of the chart.
- **description**: A brief description of the chart.
- **type**: Defines the chart type, which can be either 'application' or 'library'.
- **version**: The version of the chart itself.
- **appVersion**: The version of the application being deployed.
- **icon**: URL to the chart icon.

### values.yaml

```yaml
replicaCount: 1

serviceAccount:
  create: true
  annotations: {}

panosExporter:
  config:
    devices:
      - ip: 192.168.255.11
        username: officehours
        password: paloalto123
      - ip: 192.168.255.12
        username: officehours
        password: paloalto123
  image:
    repository: ghcr.io/cdot65/panos-exporter
    tag: latest
    pullPolicy: Always

prometheus:
  config:
    global:
      scrape_interval: 15s
      scrape_timeout: 10s
      evaluation_interval: 1m
    scrape_configs:
      - job_name: "panos_exporter"
        metrics_path: /panos
        static_configs:
          - targets:
              - 192.168.255.11
              - 192.168.255.12
        relabel_configs:
          - source_labels: ["__address__"]
            target_label: "__param_target"
          - source_labels: ["__param_target"]
            target_label: "instance"
          - target_label: "__address__"
            replacement: "panos-exporter.pan-os-telemetry.svc.cluster.local:9654"
  image:
    repository: ghcr.io/cdot65/panos-prometheus
    tag: latest
    pullPolicy: Always

grafana:
  adminPassword: paloalto123
  image:
    repository: ghcr.io/cdot65/panos-grafana
    tag: latest
    pullPolicy: Always
  service:
    type: LoadBalancer # Change to NodePort if you prefer
    port: 3000 # Default Grafana port
    nodePort: 30088 # Only needed if service.type is NodePort

ingress:
  enabled: false
  annotations: {}
  hosts:
    - host: my-grafana.example.com
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80
```

The `values.yaml` file is structured with the following key-value pairs:

- **replicaCount**: Defines the number of pod replicas.
- **serviceAccount**: Configuration for the service account.
- **panosExporter**: Configurations for the PAN-OS exporter, including device IPs, credentials, and image details.
- **prometheus**: Configurations for Prometheus, including scrape intervals, targets, relabel configs, and image details.
- **grafana**: Configurations for Grafana, including admin password, image details, service type, and port.
- **ingress**: Configurations for ingress, if enabled.
- **autoscaling**: Configurations for horizontal pod autoscaling.

These key-value pairs are used within our templates to create the appropriate Kubernetes resources, ensuring our deployment is set up correctly.

## Execution Workflow

To execute our container image build, follow these steps:

1. Clone the repository
2. Change directories to arrive at our `helm-pan-os-telemetry` project directory
3. Update the `pan-os-telemetry/values.yaml` file accordingly. Pay close attention to Grafana service type; the default is for LoadBalancer which will work for a load balancer like Metallb or Cloud Service Provider, otherwise, use NodePort.
4. Package the Helm chart with:

    ```bash
    helm package pan-os-telemetry
    ```

5. Install the Helm chart with:

    ```bash
    helm install pan-os-telemetry ./pan-os-telemetry-0.1.0.tgz --namespace pan-os-telemetry --create-namespace
    ```

6. Monitor the deployment of pods with:

    ```bash
    kubectl get pods --namespace pan-os-telemetry
    ```

7. Monitor the deployment of the networking config with:

    ```bash
    kubectl get svc --namespace pan-os-telemetry
    ```

### Screenshots

Here are some screenshots showcasing the execution of our Helm chart:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the Helm chart and customize it according to your specific requirements. Happy automating! 😄
