# -----------------------
# 1) BUILDER STAGE
# -----------------------
FROM node:20-alpine AS builder

# Install required build dependencies
RUN apk update && \
    apk add --no-cache \
      python3 \
      make \
      g++ \
      openssl \
      libc6-compat

# Create a working directory
WORKDIR /app

# Copy package files and Prisma schema
COPY backend/package*.json ./
COPY backend/prisma ./prisma

# Install Node dependencies
RUN npm ci

# Generate Prisma client here (important!)
RUN npx prisma generate

# Copy the rest of the backend source code
COPY backend/ .
COPY docker ./docker

# Build your NestJS application
RUN npm run build

# -----------------------
# 2) RUNNER STAGE
# -----------------------
FROM node:20-alpine AS runner

# Install only necessary runtime dependencies
RUN apk update && \
    apk add --no-cache \
      postgresql-client \
      python3 \
      make \
      g++ \
      openssl \
      libc6-compat

# Create a working directory
WORKDIR /app

# Copy pre-built node_modules (including generated Prisma client) from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy the compiled output, Prisma schema, and any scripts
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/docker ./docker
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/prisma ./prisma

# Generate Prisma client in runner stage
RUN npm install prisma --save-dev
RUN npx prisma generate

# Rebuild native modules if needed (e.g., bcrypt) for Alpine/musl
RUN npm rebuild bcrypt --build-from-source

# Make your startup scripts executable
RUN chmod +x /app/docker/scripts/wait-for-db.sh /app/docker/scripts/start.sh

# Expose application port
EXPOSE 3000

# Wait for DB first, then start
ENTRYPOINT ["/app/docker/scripts/wait-for-db.sh", "postgres"]
CMD ["/app/docker/scripts/start.sh"]