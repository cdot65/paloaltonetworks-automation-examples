#!/bin/bash

# Generate the root CA certificate and key
openssl req -x509 -new -nodes -days 3650 -config root_ca.cnf -out root_ca_cert.pem

# Generate the end-entity certificate and key
openssl req -new -nodes -config server.cnf -out server_csr.pem

# Sign the end-entity certificate using the root CA
openssl x509 -req -in server_csr.pem -CA root_ca_cert.pem -CAkey root_ca_key.pem -CAcreateserial -out server_cert.pem -days 365 -extfile server.cnf -extensions v3_req
