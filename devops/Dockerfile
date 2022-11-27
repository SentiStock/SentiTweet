# Use an official Python runtime as a parent image
FROM python:3.10
LABEL maintainer="SentiStock"

# Set environment varibles
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app/
COPY .. /app/
WORKDIR /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

#Creates new .env file from environmental variables if it doesn't already exist
RUN test -f .env && envsubst < .env-example > .env

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "&&", "gunicorn", "--bind", "0.0.0.0:8000", "sentitweet.backend.wsgi"]
