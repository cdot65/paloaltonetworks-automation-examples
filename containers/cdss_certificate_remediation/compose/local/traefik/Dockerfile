# compose/local/traefik/Dockerfile
FROM traefik:v2.5

# Install OpenSSL
RUN apk add --no-cache openssl

# Set up a directory for our certificates
RUN mkdir -p /etc/traefik/certs

# Copy our configuration file
COPY traefik.local.toml /etc/traefik/traefik.toml

# Copy our startup script
COPY start-traefik.sh /start-traefik.sh
RUN chmod +x /start-traefik.sh

# Generate self-signed certificate
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/traefik/certs/traefik-local.key \
    -out /etc/traefik/certs/traefik-local.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Set the entrypoint to our startup script
ENTRYPOINT ["/start-traefik.sh"]
