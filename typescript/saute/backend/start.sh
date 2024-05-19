#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Create superuser"
python manage.py createsuperuser --noinput --email "saute@test.com"

# Populate database
echo "Populate database with initial data"
python manage.py loaddata fixtures/firewall_platforms.json
python manage.py loaddata fixtures/firewalls.json
python manage.py loaddata fixtures/panorama_platforms.json
python manage.py loaddata fixtures/panoramas.json

# Load scripts
echo "Load scripts"
python manage.py load_scripts /code/saute/scripts

# Start server
echo "Starting server"
exec python manage.py runserver 0.0.0.0:8000
