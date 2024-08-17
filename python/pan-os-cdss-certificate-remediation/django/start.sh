#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Create superuser"
python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL"

# Set password for the superuser
echo "Set password for the superuser"
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
superuser = User.objects.get(username="$DJANGO_SUPERUSER_USERNAME")
superuser.set_password("$DJANGO_SUPERUSER_PASSWORD")
superuser.save()
EOF

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Start server
echo "Starting server"
exec python manage.py runserver 0.0.0.0:8000