# Saute

[![Build and Deploy](https://github.com/cdot65/saute/actions/workflows/backend.yml/badge.svg)](https://github.com/cdot65/saute/actions/workflows/backend.yml)

Saute is a self-service automation catalogue, designed to simplify the process of executing automation tasks. With no opinions on the automation technology of choice, it provides a user-friendly interface for executing automation tasks, as well as a REST API for programmatic access.

## 📚 Table of Contents

- [Saute](#saute)
  - [📚 Table of Contents](#-table-of-contents)
  - [📖 Overview](#-overview)
  - [🏗️ Application Structure](#️-application-structure)
  - [🚀 Features](#-features)
  - [📸 Screenshots](#-screenshots)
  - [🛠️ Setup Instructions](#️-setup-instructions)
  - [📝 Troubleshooting](#-troubleshooting)
  - [👥 Contribution Guidelines](#-contribution-guidelines)
  - [📜 License Information](#-license-information)

## 📖 Overview

Saute is a powerful, scalable application built on modern technologies. It seamlessly integrates a Django REST API backend with an Angular frontend, utilizing a Postgres database, Celery runners, and a container-based architecture for enhanced functionality and development efficiency.

The resulting application is a robust, scalable, and performant solution for executing automation through a GUI or REST API. It is designed to be easily deployed to your local machine or cloud platforms such as AWS or GCP.

## 🏗️ Application Structure

The application has a well-defined structure with separate directories for backend and frontend code. The key backend files include:

- `settings.py`: This file defines the configuration of our Django backend application.
- `models.py`: This file defines the database models for our application.
- `views.py`: This Django file handles API endpoints and request-response lifecycle.
- `tasks.py`: This file defines Celery tasks for asynchronous execution.

The key frontend files include:

- `app.module.ts`: This is the entry point for the Angular frontend.
- `app-routing.module.ts`: This file defines the routes for the frontend.
- `widgets.module.ts`: This file defines the widgets for the dashboard.
- `create-script.component.ts`: Defines the logic for the ChatGPT integration.

The backend code is primarily organized in the Django application, located in the `/backend` directory. The Angular code resides in a separate `/frontend` directory. The two applications communicate through the backend's Django REST API.

## 🚀 Features

- **Django REST API**: Backend server that handles requests and database operations.
- **Angular frontend**: User interface and frontend logic.
- **Postgres database**: Robust relational database for data storage.
- **Celery runners**: Asynchronous task execution to improve performance.
- **Container-based architecture**: Simplified development and deployment process.

## 📸 Screenshots

Here's a look at our application:

Taking a snapshot of a firewall before and after a change is a breeze:

![Taking Snapshots](docs/images/snapshots.gif)

Let ChatGPT explain the differences between the snapshots and provide suggestions on next steps:

![ChatGPT](docs/images/change-analysis.gif)

Using the ChatGPT integration to generate a script for a firewall change:

![ChatGPT Integration](docs/images/create-script.gif)

## 🛠️ Setup Instructions

Here are the steps to set up the application in a local development environment:

1. Clone the repository and navigate to the project directory.
2. Rename `backend/.env.example` to `backend/.env` and update the file's contents accordingly.
3. Run the following command to build and start the services:

   ```bash
   docker-compose up -d --build
   ```

4. Once the services are up and running, execute the database migrations and give it a little restart to make everyone happy:

   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose restart
   ```

5. Create a superuser account:

   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

6. The backend application should now be accessible at `localhost:8000`, the frontend will be available at `localhost:8080`.

## 📝 Troubleshooting

If there are any issues with the application, its likely that checking the backend and worker containers are going to provide the most valuable information. To do this, run the following commands:

```bash
docker-compose logs backend
docker-compose logs worker
```

The frontend container will likely always be running, but if there are any issues with it, you can check the logs with the following command:

```bash
docker-compose logs frontend
```

More times than not I have found myself working just fine within the frontend angular application, only to find that the backend is throwing errors. If you are having issues with the frontend communicating with the backend (cannot login, no inventory or jobs found), it is worth checking the backend logs to see if there are any errors being thrown.

## 👥 Contribution Guidelines

We welcome and appreciate any contributions. Please follow these steps:

1. Fork the project repository.
2. Create a new branch for your feature or fix.
3. Make your changes and commit them to your branch.
4. Submit a pull request, and our team will review your contribution.

## 📜 License Information

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file in the project root.
