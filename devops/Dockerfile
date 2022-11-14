# Use an official Python runtime as a parent image
FROM python:3.10
LABEL maintainer="SentiStock"

# Set environment varibles
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

RUN apt-get update

# RUN apt-get install mariadb-server -y

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt

# Set the working directory to /app/
COPY ./sentitweet/ /app/
# COPY ./devops/mysqlssl/ /app/mysqlssl/
WORKDIR /app/

EXPOSE 8000

# RUN python backend/manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000 && gunicorn --bind 0.0.0.0:8000 sentitweet.backend.wsgi
