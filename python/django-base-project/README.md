# Django Base Template 📚

This README provides an overview of our Python project and guides you through the setup and execution process. 🚀

## Table of Contents

- [Django Base Template 📚](#django-base-template-)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Installing a Container Runtime Engine](#installing-a-container-runtime-engine)
  - [Django Project Structure](#django-project-structure)
  - [Docker and Docker-Compose](#docker-and-docker-compose)
    - [Explanation of the `docker-compose.yaml`:](#explanation-of-the-docker-composeyaml)
  - [Features](#features)
  - [Execution Workflow](#execution-workflow)
    - [Screenshots](#screenshots)

## Overview

Our Python Django project aims to be the base template for all Django web applications. We will ship the application as Docker containers with docker-compose, providing a simple-to-manage yet scalable application architecture 🎯

## Prerequisites

Before getting started, ensure that you have the following prerequisites installed on your local machine:

- Docker

## Setup

### Installing a Container Runtime Engine

- Installing Docker on [Linux](https://docs.docker.com/desktop/install/linux-install/), [macOS](https://docs.docker.com/desktop/install/mac-install/), or [Windows](https://docs.docker.com/desktop/install/windows-install/)

## Django Project Structure

Our Django project is structured as follows:

```bash
❯ tree -L 2
.
├── README.md
├── django
│   ├── Dockerfile
│   ├── accounts
│   ├── django_project
│   ├── manage.py
│   ├── requirements.txt
│   ├── start.sh
│   ├── static
│   └── staticfiles
├── docker-compose.yaml
├── poetry.lock
├── pyproject.toml
└── tasks.py
```

- `django/`: Contains the main Django project.
  - `Dockerfile`: Docker configuration for setting up the Django application.
  - `accounts/`: Django application for user accounts.
  - `django_project/`: The main Django project directory.
  - `manage.py`: Django's command-line utility for administrative tasks.
  - `requirements.txt`: List of dependencies to be installed using pip.
  - `start.sh`: Shell script for starting the Django application.
  - `static/`: Directory to store static files.
  - `staticfiles/`: Directory for collected static files.
- `docker-compose.yaml`: Docker Compose configuration to start up the whole project.
- `poetry.lock` and `pyproject.toml`: Poetry configuration files for dependencies.
- `tasks.py`: Script for various automation tasks using Invoke.

## Docker and Docker-Compose

Explanation of the `Dockerfile`:

```Dockerfile
# pull base image
FROM python:3.11.2-slim-bullseye

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install locales package
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/*

# generate and set the en_US.UTF-8 locale
RUN echo "en_US.UTF-8 UTF-8" >>/etc/locale.gen
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# set work directory
WORKDIR /code

# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add startup script
COPY start.sh .

# Make the start script executable
RUN chmod +x start.sh

# copy project
COPY . .
```

### Explanation of the `docker-compose.yaml`:

```yaml
services:
  web:
    build:
        context: ./django
        dockerfile: Dockerfile
    command: /code/start.sh
    volumes:
      - ./django:/code
    environment:
      - "DJANGO_SECRET_KEY=XNaZeqVx7B8o4p9K9C_4ICD9-c9fCeEnRnW6JR-2MAe8-xmuNQc"
      - "SENDGRID_API_KEY=this-is-just-a-placeholder"
      - "DJANGO_DEBUG=True"
    ports:
      - 8000:8000
    depends_on:
      - db
    env_file:
       - ./django/.env

  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - "POSTGRES_HOST_AUTH_METHOD=trust"
    env_file:
      - ./django/.env
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

- `services`: Defines the services that will be run in the Docker environment.
  - `web`: Specifies the configuration for the Django web application service.
    - `build`:
      - `context`: Specifies the build context, in this case, the `./django` directory.
      - `dockerfile`: Points to the `Dockerfile` located in the `./django` directory.
    - `command`: Command to start the Django application using the `start.sh` script.
    - `volumes`: Mounts the `./django` directory on the host to the `/code` directory in the container.
    - `environment`: Environment variables required by the Django application, for example, `DJANGO_SECRET_KEY`, `SENDGRID_API_KEY`, and `DJANGO_DEBUG`.
    - `ports`: Maps port 8000 on the host to port 8000 in the container to access the Django application via `http://localhost:8000`.
    - `depends_on`: Specifies the dependency on the `db` service, ensuring that the database service is started before the web application.
    - `env_file`: Specifies the environment file (`./django/.env`) that contains additional environment variables.

  - `db`: Specifies the configuration for the PostgreSQL database service.
    - `image`: The Docker image for PostgreSQL version 14.
    - `volumes`: Mounts a volume for persistent database storage.
    - `environment`: Environment variables required for the PostgreSQL database service, for example, `POSTGRES_HOST_AUTH_METHOD=trust`.
    - `env_file`: Specifies the environment file (`./django/.env`) that contains additional environment variables.
    - `ports`: Maps port 5432 on the host to port 5432 in the container for database access.

- `volumes`: Persistent storage definitions.
  - `postgres_data`: Named volume for PostgreSQL data storage.

## Features

This Django base template includes several powerful features to enhance your web application:

- **Integration with SendGrid's API**: This enables sending transactional emails effortlessly using SendGrid.
- **Custom Built Role-Based Access Control (RBAC)**: For more granular access control within your application.
- **Django REST framework (DRF)**: Added to allow for the creation of REST API applications.
- **Default User Credentials**: For easier initial setup, the default user is `admin` and the password is `paloalto123`.

## Execution Workflow

To execute our docker-compose file, follow these steps:

1. Build the container images with `docker-compose build`
2. Start the container images with `docker-compose up -d`
   1. Logs for troubleshooting can be found with `docker-compose logs`
3. Access the Django admin panel at `http://localhost:8000/admin`
4. Start building your applications with `docker-compose exec web python manage.py startapp xyz`

### Screenshots

Here are some screenshots showcasing the execution of our Python script:

![Screenshot 1](screenshots/screenshot1.png)
![Screenshot 2](screenshots/screenshot2.png)

Feel free to explore the script and customize it according to your specific requirements. Happy automating! 😄
