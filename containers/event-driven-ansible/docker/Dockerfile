# Use Fedora Base Image
FROM fedora:latest

# Update package index and install OpenJDK, Python, Pip, GCC, and Python development headers
RUN dnf update -y
RUN dnf install -y java-17-openjdk python3.12 python3-pip maven gcc python3.12-devel
RUN dnf groupinstall -y "Development Tools"
RUN dnf install -y redhat-rpm-config libffi-devel openssl-devel
RUN dnf clean all

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/jre-17-openjdk

# Install Ansible, ansible-rulebook (with no binary jpy), and ansible-runner
RUN pip3 install ansible ansible-runner aiohttp==3.9.0b0
RUN pip3 install ansible-rulebook --no-binary jpy

# Install any dependencies and Ansible Collection
RUN pip3 install pan-os-python xmltodict
RUN ansible-galaxy collection install paloaltonetworks.panos

# Set working directory
WORKDIR /ansible/eda
