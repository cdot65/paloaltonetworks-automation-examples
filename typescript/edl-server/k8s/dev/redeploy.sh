#!/usr/bin/env bash

docker compose build frontend && docker tag edl-server-frontend ghcr.io/cdot65/edl-frontend:dev && docker push ghcr.io/cdot65/edl-frontend:dev && kubectl delete pod -n dev-edl -l app=frontend
docker compose build backend && docker tag edl-server-backend ghcr.io/cdot65/edl-backend:dev && docker push ghcr.io/cdot65/edl-backend:dev && kubectl delete pod -n dev-edl -l app=backend

kubectl apply -f k8s/dev/00-namespace.yaml \
&& kubectl apply -f k8s/dev/01-configmap.yaml \
&& kubectl apply -f k8s/dev/02-secret.yaml \
&& kubectl apply -f k8s/dev/03-postgres.yaml \
&& kubectl apply -f k8s/dev/04-backend.yaml \
&& kubectl apply -f k8s/dev/05-frontend.yaml \
&& kubectl apply -f k8s/dev/06-traefik.yaml \
&& kubectl apply -f k8s/dev/07-ingress.yaml \
&& kubectl apply -f k8s/dev/08-ingressclass.yaml \
&& kubectl apply -f k8s/dev/09-rbac.yaml \
&& kubectl apply -f k8s/dev/10-traefik-svc.yaml
