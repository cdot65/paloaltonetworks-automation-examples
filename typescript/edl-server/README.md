# EDL Management Server

A NestJS-based server for managing External Dynamic Lists (EDLs) with support for IP addresses, URLs, and domains. Built with Docker, PostgreSQL, and Traefik for modern deployment and scalability.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
    - [Environment Setup](#environment-setup)
    - [TLS Certificates](#tls-certificates)
    - [Deployment](#deployment)
- [Usage](#usage)
    - [Creating EDL Lists](#creating-edl-lists)
    - [Managing EDL Entries](#managing-edl-entries)
    - [Accessing EDLs](#accessing-edls)
- [Development](#development)

## Features
- Support for multiple EDL types:
    - IP addresses (IPv4 and IPv6)
    - URLs
    - Domains
- RESTful API for EDL management
- Plaintext and JSON output formats
- TLS support with self-signed certificates
- Docker-based deployment
- PostgreSQL database backend
- Traefik load balancer

## Prerequisites
- Docker
- Docker Compose
- curl (for API examples)

## Getting Started

### Environment Setup
1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/edl-server.git
    cd edl-server
    ```

2. Create your environment file:

    ```bash
    cp .env.example .env
    ```

3. Update the `.env` file with your desired values:

    ```env
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=your_secure_password
    POSTGRES_DB=edl_db
    POSTGRES_PORT=5432
    FRONTEND_URL=https://localhost
    ```

### TLS Certificates
The server uses TLS certificates for secure communication. You can:

1. Use the existing self-signed certificates:

    ```bash
    mkdir -p certs
    ```

2. Or generate new ones:

    ```bash
    chmod +x scripts/generate-tls-cert.sh
    ./scripts/generate-tls-cert.sh
    ```

### Deployment
1. Start the application:

    ```bash
    docker compose up -d
    ```

2. Verify all services are running:

    ```bash
    docker compose ps
    ```

3. Access the web application at:

    ```
    https://localhost/
    ```

Note: Your browser will show a security warning due to the self-signed certificate. This is expected in development environments.

## Usage

### Creating EDL Lists

1. Create an IP address list:

    ```bash
    curl -X POST 'https://localhost/api/v1/edl/lists' \
    -H 'Content-Type: application/json' \
    -d '{
      "name": "malicious-ips",
      "description": "Known malicious IP addresses",
      "type": "IP"
    }'
    ```

2. Create a URL list:

    ```bash
    curl -X POST 'https://localhost/api/v1/edl/lists' \
    -H 'Content-Type: application/json' \
    -d '{
      "name": "blocked-urls",
      "description": "Blocked website URLs",
      "type": "URL"
    }'
    ```

### Managing EDL Entries

1. Add an IPv4 entry:

    ```bash
    curl -X POST 'https://localhost/api/v1/edl/entries' \
    -H 'Content-Type: application/json' \
    -d '{
      "address": "192.168.1.100",
      "comment": "Known C2 server",
      "type": "IP",
      "listName": "malicious-ips"
    }'
    ```

2. Add an IPv6 entry:

    ```bash
    curl -X POST 'https://localhost/api/v1/edl/entries' \
    -H 'Content-Type: application/json' \
    -d '{
      "address": "2406:e500:4010::/48",
      "comment": "Malicious IPv6 range",
      "type": "IP",
      "listName": "malicious-ips"
    }'
    ```

3. Add a URL entry:

    ```bash
    curl -X POST 'https://localhost/api/v1/edl/entries' \
    -H 'Content-Type: application/json' \
    -d '{
      "address": "https://malicious-site.com/path",
      "comment": "Phishing website",
      "type": "URL",
      "listName": "blocked-urls"
    }'
    ```

### Accessing EDLs

1. Get plaintext format (for firewall consumption):

    ```bash
    curl -X GET 'https://localhost/api/v1/edl/malicious-ips/plaintext'
    ```

2. Get JSON format:

    ```bash
    curl -X GET 'https://localhost/api/v1/edl/lists/malicious-ips'
    ```

## Development

### Debugging
View service logs:

```bash
# All services
docker compose logs

# Specific service
docker compose logs backend
```

### Stopping the Application

```bash
docker compose down
```

To remove all data (including database):

```bash
docker compose down -v
```

### Certificate Management
If you need to update certificates after deployment:
1. Generate new certificates:

    ```bash
    ./scripts/generate-tls-cert.sh
    ```

2. Restart Traefik:

    ```bash
    docker compose restart traefik
    ```

## Note
This is a development setup with self-signed certificates. For production deployment:
- Use proper SSL certificates from a trusted CA
- Disable the Traefik dashboard or secure it
- Configure proper authentication
- Set up backup strategies
- Implement rate limiting