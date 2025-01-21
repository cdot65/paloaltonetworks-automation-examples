# pull base image
FROM python:3.11.2-slim-bullseye

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install locales package
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/*

# generate and set the en_US.UTF-8 locale
RUN echo "en_US.UTF-8 UTF-8" >>/etc/locale.gen
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

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
