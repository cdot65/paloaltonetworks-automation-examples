#!/bin/sh
# compose/local/traefik/start-traefik.sh

set -e

# Check if the certificate exists, if not, generate it
if [ ! -f /etc/traefik/certs/traefik-local.crt ] || [ ! -f /etc/traefik/certs/traefik-local.key ]; then
    echo "Generating self-signed certificate..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/traefik/certs/traefik-local.key \
        -out /etc/traefik/certs/traefik-local.crt \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
fi

# Start Traefik
exec traefik
