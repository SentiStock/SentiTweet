# Use an official Python runtime as a parent image
FROM python:3.10
LABEL maintainer="SentiStock"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

RUN apt-get update

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt

# Set the working directory to /app/
COPY ./sentitweet/ /app/
WORKDIR /app/

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000 && gunicorn --bind 0.0.0.0:8000 sentitweet.backend.wsgi
