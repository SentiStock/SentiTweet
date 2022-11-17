# SentiTweet
Interactive dashboard of analyzed Tweets correlated to stocks

## Requirements
- docker
- Make

## Setup
1. Duplicate the sentitweet/.env-example file and rename to ```sentitweet/.env```. Fill in the needed environment variables
2. In the root of the project there are multiple Make commands:
    - ```make up``` --> to start the app
    - ```make stop``` --> to stop the app
    - ```make down``` --> to delete the app (in docker)
    - ```make logs``` --> to view the app activity
    - ```make migrate``` --> to update the database with all the columns
3. When running ```make up``` the app is running on localhost port 8000 --> ```127.0.0.1:8000```
4. Only run ```make migrate``` when new database columns have been created
5. The following Make command are only for development
    - ```make makemigrations``` --> to update mirgation files when changes have been made
    - To get a superuser first run ```make shell``` and then ```pyhton manage.py createsuperuser```