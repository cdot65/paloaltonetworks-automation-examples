# Django REST API Base Template

## Overview

A Docker-based Django REST Framework starter project with PostgreSQL, Celery task queue, custom user authentication, and auto-generated API documentation. It uses Django 4.x with DRF token and session authentication, django-allauth for registration, drf-spectacular for OpenAPI/Swagger schema generation, and WhiteNoise for static file serving. The project includes a custom user model with circular profile image processing via Pillow, Docker Compose for local orchestration, and Invoke tasks for build automation. Intended as a starting point for REST API applications that may integrate with Palo Alto Networks automation tooling.

## Prerequisites

- Docker and Docker Compose
- Python 3.10+ and Poetry (for local development outside Docker)

## Quickstart

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cdot65/paloaltonetworks-automation-examples.git
   cd paloaltonetworks-automation-examples/python/general/django-base
   ```

2. **Create and activate a virtual environment (for local dev tools):**

   ```bash
   poetry install
   poetry shell
   ```

   > **Tip -- What is a virtual environment?** A virtual environment is an isolated Python installation that keeps project dependencies separate from your system Python. This prevents version conflicts between projects.

3. **Configure environment variables:**

   ```bash
   cp django/.env.example django/.env
   ```

   Edit `django/.env` with your settings.

4. **Start the application:**

   ```bash
   docker compose up --build
   ```

5. **Access the application:**

   Open `http://localhost:8000/admin/` -- default superuser is `admin` / `paloalto123`.

## Configuration

The Django `.env` file (`django/.env`) uses the following variables:

```
DJANGO_ALLOWED_HOSTS=['localhost', '127.0.0.1', '*']
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=your-secret-key-here
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_password
POSTGRES_DB=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
CELERY_BROKER_URL="redis://redis:6379/0"
CELERY_RESULT_BACKEND="redis://redis:6379/0"
DJANGO_SUPERUSER_PASSWORD="paloalto123"
DJANGO_SUPERUSER_USERNAME="admin"
```

| Variable | Required | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | Yes | Django secret key for cryptographic signing |
| `DJANGO_DEBUG` | No | Enable debug mode (default: False) |
| `POSTGRES_USER` | Yes | PostgreSQL username |
| `POSTGRES_PASSWORD` | Yes | PostgreSQL password |
| `POSTGRES_DB` | Yes | PostgreSQL database name |
| `POSTGRES_HOST` | Yes | PostgreSQL host (use `db` in Docker Compose) |
| `POSTGRES_PORT` | Yes | PostgreSQL port (default: 5432) |
| `CELERY_BROKER_URL` | No | Redis URL for Celery broker |
| `CELERY_RESULT_BACKEND` | No | Redis URL for Celery result backend |
| `DJANGO_SUPERUSER_USERNAME` | No | Auto-created superuser username |
| `DJANGO_SUPERUSER_PASSWORD` | No | Auto-created superuser password |

**Security note:** Never commit `.env` files with real secrets to version control.

## Usage

**Start all services:**

```bash
docker compose up --build
```

**Build Docker image via Invoke:**

```bash
invoke build
```

**Run container locally:**

```bash
invoke local
```

**Get shell access to the container:**

```bash
invoke shell
```

### Expected Output

On startup, Docker Compose outputs:

```
Apply database migrations
Operations to perform:
  Apply all migrations: accounts, admin, auth, contenttypes, sessions, sites
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying accounts.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
Create superuser
Superuser created successfully.
Set password for the superuser
Collect static files
168 static files copied to '/code/staticfiles'.
Starting server
Watching for file changes with StatReloader
```

### API Endpoints

- `/admin/` -- Django admin interface
- `/api/v1/dj-rest-auth/` -- Authentication endpoints (login, logout, password reset)
- `/api/v1/dj-rest-auth/registration/` -- User registration
- `/api/schema/` -- OpenAPI schema (JSON)
- `/api/schema/swagger` -- Swagger UI documentation
- `/api/schema/redoc` -- ReDoc documentation

## Project Structure

```
django-base/
  docker-compose.yaml          # Web + PostgreSQL service definitions
  pyproject.toml               # Poetry project config (Django 4.x, psycopg2)
  tasks.py                     # Invoke tasks for Docker build/run/shell
  django/
    Dockerfile                 # Python 3.11 slim image with locale support
    start.sh                   # Entrypoint: migrations, superuser, collectstatic, runserver
    manage.py                  # Django management command entry point
    requirements.txt           # Pinned Python dependencies (50+ packages)
    .env.example               # Environment variable template
    django_project/
      settings.py              # DRF, Celery, PostgreSQL, WhiteNoise, CORS config
      urls.py                  # Admin, auth, OpenAPI schema routes
      celery.py                # Celery app configuration with Redis broker
      wsgi.py                  # WSGI entry point
      asgi.py                  # ASGI entry point
    accounts/
      models.py                # CustomUser with profile image (circular crop via Pillow)
      admin.py                 # Custom user admin registration
      forms.py                 # User creation/change forms with image handling
      migrations/              # Database migration files
```

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `could not connect to server: Connection refused` | PostgreSQL not ready | Wait for db container to initialize; check `docker compose logs db` |
| `KeyError: 'DJANGO_SECRET_KEY'` | Missing environment variable | Ensure `django/.env` exists with all required variables |
| `ModuleNotFoundError: No module named 'environs'` | Dependencies not installed in container | Rebuild with `docker compose up --build` |
| SSL certificate errors | N/A for local dev | Not applicable; this project runs locally |
| Connection refused on port 8000 | Container not running or crashed | Run `docker compose up` and check for startup errors in logs |
| `CSRF verification failed` | Untrusted origin | Add your domain to `CSRF_TRUSTED_ORIGINS` in `settings.py` |
| Profile image upload fails with `AttributeError` | Pillow version incompatibility | `Image.ANTIALIAS` was removed in Pillow 10; downgrade to Pillow 9.x or update code to `Image.LANCZOS` |
