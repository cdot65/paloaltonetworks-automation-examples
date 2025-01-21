# pull base image
FROM python:3.11.2-slim-bullseye

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory
WORKDIR /code

# install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add startup script
COPY start.sh .

# Make the start script executable
RUN chmod +x start.sh

# copy project
COPY . .
