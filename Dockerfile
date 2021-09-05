# Pull base image
FROM python:3.6
#FROM python:3.7-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy project
COPY ./ /app/

# Install dependencies
RUN apt-get update && apt-get install tk-dev && rm -r /var/lib/apt/lists/*
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r /app/requirements.txt
