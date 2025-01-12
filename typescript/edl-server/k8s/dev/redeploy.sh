#!/usr/bin/env bash

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
