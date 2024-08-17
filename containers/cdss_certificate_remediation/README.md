# CDSS Certificate Remediation

PAN-OS CDSS Certificate Remediation

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Getting Started

### Installing Docker

Before you begin, you'll need to install Docker on your system. Docker allows you to run applications in containers, making it easy to set up and run our project.

#### For Windows:
1. Download Docker Desktop for Windows from the [official Docker website](https://www.docker.com/products/docker-desktop).
2. Follow the installation instructions provided.
3. Once installed, start Docker Desktop.

#### For macOS:
1. Download Docker Desktop for Mac from the [official Docker website](https://www.docker.com/products/docker-desktop).
2. Follow the installation instructions provided.
3. Once installed, start Docker Desktop.

### Docker Compose

This project uses Docker Compose to define and run multi-container Docker applications. We have two Docker Compose files:

- `docker-compose.local.yml`: For local development
- `docker-compose.production.yml`: For production deployment

## Setting Up the Project

Follow these steps to set up and run the project locally:

1. Build the Docker images:
    ```
    docker compose -f docker-compose.local.yml build
    ```
    This command builds the Docker images defined in the docker-compose file.

2. Start the Docker containers:
    ```
    docker compose -f docker-compose.local.yml up -d
    ```
    This command starts the Docker containers in detached mode.

3. Run database migrations:
    ```
    docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
    ```
    This command applies any pending database migrations.

4. Create a superuser:
    ```
    docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
    ```
    This command creates an admin user for the Django admin interface.

5. Collect static files:
    ```
    docker compose -f docker-compose.local.yml run --rm django python manage.py collectstatic
    ```
    This command collects all static files into a single directory for serving.

After completing these steps, you can access the application by navigating to `localhost:8000` in your web browser.

## Environment Variables

The Django application uses environment variables for configuration. These are stored in `.env` files in the `.envs` directory.

### Local Development

For local development, the following environment files are used; adjust as you see fit:

#### .envs/.local/.django
```
USE_DOCKER=yes
IPYTHONDIR=/app/.ipython
REDIS_URL=redis://redis:6379/0
CELERY_FLOWER_USER=TVESqMVdiKYaZMkjyeUbbyaXunAugvNU
CELERY_FLOWER_PASSWORD=Q87yx6dLEHofc00ObVWg7TCW1godKiODxMMN7UkygLTjW4UdCBKv00YSW6TjwZnR
```

#### .envs/.local/.postgres
```
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=cdss_certificate_remediation
POSTGRES_USER=mUCXwAwCFRJsQOMuHxeenmfkVsTEvgyd
POSTGRES_PASSWORD=EuN3KVIGbHkPqvOPMrNuq38MCF953dfzqyFQ1QMCJANyxVZqcVOQndkZImFppeMe
```

### Production Deployment

For production deployment, you'll need to create a `production` directory in the `.envs` folder and add the following files:

#### .envs/.production/.django
```
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=i1iK8JTMv9dRa6WLtWLCLFed51MDQ2sBw57JVxLISznj3LHPjQixo0hiwyzBXmfm
DJANGO_ADMIN_URL=an2jcn9QmCyUSEuN3IQJlHWPO6tw0j4c/
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,*
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_ACCOUNT_ALLOW_REGISTRATION=True
WEB_CONCURRENCY=4
REDIS_URL=redis://redis:6379/0
CELERY_FLOWER_USER=TVESqMVdiKYaZMkjyeUbbyaXunAugvNU
CELERY_FLOWER_PASSWORD=DclJlnny6Gzf5pb78H85ruozvwuFIcsKrGWnlsfMMaPzIZzogaBDKYYiXMp61MHk
```

#### .envs/.production/.postgres
```
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=cdss_certificate_remediation
POSTGRES_USER=mUCXwAwCFRJsQOMuHxeenmfkVsTEvgyd
POSTGRES_PASSWORD=MMzND0CvDiSQRoSUpZQhi8YHGcbEi8B5jYRz0aDZlQhnxX5bI2mlGYZibqCi1OQU
```

### Traefik Configuration for Production

For production deployment with a valid domain name, you'll need to update the Traefik configuration file located at `compose/production/traefik/traefik.yml`. Replace all instances of `example.com` with your actual domain name. This is necessary for registering a new TLS certificate through acme.sh.

Key areas to update in the Traefik configuration:

1. The email address for Let's Encrypt notifications
2. The `Host` rules for the web-secure-router and flower-secure-router
3. The `Host` rule for the web-media-router

After making these changes, you can use the `docker-compose.production.yml` file to deploy your application in a production environment with TLS encryption.

## Deployment

For detailed information on deploying this application, please refer to the [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

## Additional Information

For more detailed information about the project settings and structure, please refer to the [cookiecutter-django documentation](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).
