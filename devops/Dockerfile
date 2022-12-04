# Use an official Python runtime as a parent image
FROM python:3.10
LABEL maintainer="SentiStock"

# Set environment varibles
ENV PYTHONUNBUFFERED 1

# Update ap-get
RUN apt-get update

# Install cron for running cronjobs
RUN apt-get -y install cron

# Set the working directory to /app/
COPY .. /app/
WORKDIR /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

# Add our python cronjobs to machine cronjobs
# Start cron
# Run the server
CMD python manage.py crontab add && cron && python manage.py runserver 0.0.0.0:8000 && gunicorn --bind 0.0.0.0:8000 sentitweet.backend.wsgi
