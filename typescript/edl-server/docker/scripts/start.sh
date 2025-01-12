#!/bin/sh
set -e

echo "Current working directory: $(pwd)"
echo "Files in current directory: $(ls -la)"

# Initialize and apply migrations
echo "Initializing database migrations..."
npx prisma migrate reset --force

echo "Creating initial migration..."
npx prisma migrate dev --name init_schema --create-only

echo "Applying migrations..."
npx prisma migrate deploy

echo "Generating Prisma client..."
npx prisma generate

# Start the application
echo "Starting the application..."
npm run start:prod