#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Create superuser"
python manage.py createsuperuser --noinput --email "automation@example.com"

# Set password for the superuser
echo "Set password for the superuser"
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
superuser = User.objects.get(email="automation@example.com")
superuser.set_password("this-is-just-a-placeholder")
superuser.save()
EOF

# Populate database
# echo "Populate database with initial data"
# python manage.py loaddata fixtures/devicetype.json
# python manage.py loaddata fixtures/device.json
# python manage.py loaddata fixtures/profiles.json

# Load scripts
# echo "Load scripts"
# python manage.py load_scripts /code/panosupgradeweb/scripts

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Start server
echo "Starting server"
exec python manage.py runserver 0.0.0.0:8000
