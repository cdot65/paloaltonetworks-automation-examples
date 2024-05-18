FROM python:3.11-slim

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
LABEL name="ghcr.io/cdot65/pan-ansible:latest" \
    maintainer="cremsburg.dev@gmail.com" \
    description="Docker container for PAN-OS and Panorama" \
    license="Apache 2.0" \
    url="https://github.com/cdot65/pan-ansible" \
    build-date="20230406"

# ---------------------------------------------------------------------------
# Install dependencies
# ---------------------------------------------------------------------------
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    sudo \
    git \
    curl \
    vim \
    less \
    zsh
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# Create user
# ---------------------------------------------------------------------------
RUN useradd -m ansible
RUN echo "ansible ALL=(ALL) NOPASSWD: ALL" >>/etc/sudoers

# ---------------------------------------------------------------------------
# Switch to ansible user
# ---------------------------------------------------------------------------
USER ansible

# ---------------------------------------------------------------------------
# Set up Zsh shell
# ---------------------------------------------------------------------------
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
SHELL ["/bin/zsh", "-c"]

# ---------------------------------------------------------------------------
# Install Poetry
# ---------------------------------------------------------------------------
RUN curl -sSL https://install.python-poetry.org | python3 -

# ---------------------------------------------------------------------------
# Change directory to /home/ansible
# ---------------------------------------------------------------------------
WORKDIR /home/ansible
COPY pyproject.toml pyproject.toml

# ---------------------------------------------------------------------------
# Setup user's environment
# ---------------------------------------------------------------------------
ENV POETRY_VIRTUALENVS_PATH="/home/ansible/venv"
ENV ANSIBLE_CONFIG /home/ansible/ansible.cfg

# ---------------------------------------------------------------------------
# Install packages and Ansible Galaxy collections
# ---------------------------------------------------------------------------
RUN echo 'export PATH="/home/ansible/.local/bin:$PATH"' >>~/.zshrc
RUN source ~/.zshrc
RUN /home/ansible/.local/bin/poetry install
RUN /home/ansible/.local/bin/poetry run ansible-galaxy collection install paloaltonetworks.panos
RUN echo 'source $POETRY_VIRTUALENVS_PATH/pan-ansible-*/bin/activate' >>~/.zshrc
