FROM jenkins/inbound-agent:latest

USER root

# Install kubectl
RUN apt-get update && \
    apt-get install -y apt-transport-https gnupg2 curl ca-certificates && \
    curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add - && \
    apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download kubectl binary
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Make kubectl executable and move it to a directory in PATH
RUN chmod +x kubectl && mv kubectl /usr/local/bin/

USER jenkins