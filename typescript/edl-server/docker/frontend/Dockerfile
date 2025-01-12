# -----------------------
# 1) BUILDER STAGE
# -----------------------
FROM node:20-alpine AS builder

# (Optional) Install Python, make, g++, etc. if needed for building certain npm packages
# For typical Angular apps, you might not need them—only if you have packages that require native add-ons.
# But if you encounter errors like node-gyp build failures, uncomment and adjust:
# RUN apk update && \
#     apk add --no-cache python3 make g++

# Create app directory
WORKDIR /app

# Copy package.json and package-lock.json to leverage Docker cache
COPY frontend/package*.json ./

# Install project dependencies
RUN npm ci

# Copy the entire Angular application code
COPY frontend/ .

# Build the Angular application in production mode
RUN npm run build -- --configuration production

# -----------------------
# 2) RUNNER STAGE (Using Nginx to serve the static files)
# -----------------------
FROM nginx:alpine AS runner

# Copy nginx configuration
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built Angular app from the builder stage to Nginx's web root
COPY --from=builder /app/dist/frontend/browser /usr/share/nginx/html

# Expose port 80 (default HTTP port)
EXPOSE 80

# Start Nginx, replacing the default config with one that enables gzip
CMD ["nginx", "-g", "daemon off;"]