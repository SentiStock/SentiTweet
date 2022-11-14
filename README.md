# SentiTweet
Interactive dashboard of analyzed Tweets correlated to stocks

## Requirements
- python 3.10
- pip3
- docker
- Make

## Setup
1. Create your /venv in the root of the project --> ```pyhotn3 -m venv venv```
2. Duplicate the sentitweet/.env-example file and rename to ```sentitweet/.env```. Fill in the needed environment variables
3. In the root of the project there are multiple Make commands:
    - ```make up``` --> to start the app
    - ```make stop``` --> to stop the app
    - ```make down``` --> to delete the app (in docker)
    - ```make logs``` --> to view the app activity
    - ```make migrate``` --> to update the database with all the columns
4. When running ```make up``` the app is running on localhost port 8000 --> ```127.0.0.1:8000```
5. Only run ```make migrate``` when new database columns have been created
6. The following Make command are only for development
    - ```make makemigrations``` --> to update mirgation files when changes have been made
    - To get a superuser first run ```make shell``` and then ```pyhton manage.py createsuperuser```