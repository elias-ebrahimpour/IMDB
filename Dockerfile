# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app
RUN pip install --upgrade pip && pip install -r requirements.txt