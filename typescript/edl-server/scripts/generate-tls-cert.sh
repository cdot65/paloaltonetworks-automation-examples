#!/bin/bash
# Generate fresh certificates

# Create certs directory
mkdir -p certs

# Generate CA private key
openssl genrsa -out certs/key.pem 4096

# Generate certificate
openssl req -x509 \
    -new \
    -nodes \
    -key certs/key.pem \
    -sha256 \
    -days 730 \
    -out certs/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,DNS:edl.cdot.io"

# Verify the certificate
echo "Verifying certificate..."
openssl x509 -in certs/cert.pem -text -noout

# Set permissions
chmod 644 certs/cert.pem
chmod 600 certs/key.pem

echo "Certificate generation complete. Testing files..."
if [ -f certs/cert.pem ] && [ -f certs/key.pem ]; then
    echo "Certificate files exist and are readable"
    ls -l certs/
else
    echo "Error: Certificate files are missing"
    exit 1
fi