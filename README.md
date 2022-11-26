# SentiTweet
Interactive dashboard for comprehensive analysis of Twitter tweets

## Peoject Status
Milestone 1 MUST HAVE

Newest release - none


## Table of Contents
- [SentiTweet](#sentitweet)
  - [Peoject Status](#peoject-status)
  - [Table of Contents](#table-of-contents)
- [About](#about)
  - [Project aim](#project-aim)
  - [Features](#features)
  - [Technologies](#technologies)
  - [Project Roadmap](#project-roadmap)
  - [Documentation](#documentation)
  - [Example of use](#example-of-use)
    - [User story 1](#user-story-1)
    - [User story 2](#user-story-2)
- [Getting started](#getting-started)
  - [Usage](#usage)
    - [Requirements](#requirements)
  - [Installation](#installation)
    - [Lanuch](#lanuch)
  - [Development](#development)
  - [Contributing](#contributing)
    - [Mindset](#mindset)
    - [Branching](#branching)
    - [Coding guidelines](#coding-guidelines)


# About

## Project aim
We live in a world that contains an overwhelming amount of information, ambiguity, and uncertainty. It is hard to stay up-to-date with current trends and market opinions. To extract only what truly matters, one needs to have tremendous experience, excellent technical skills, and secrifice time and money to get desired insights. _That's frustrating._

_And we also have been there._

That's why we have created this platform. We hope that with this tool, everyone will escape the information overload, save weeks tracking and searching for inrelevant things, and **only focus on most ROI insights from Twitter tweets**.

## Features

## Technologies
- [X] Django 4.1
  - [ ] Allauth 0.51
  - [X] Datta-able 1.0.9
- [X] Python 3.10
  - [ ] Numpy 1.23
  - [ ] Pandas 1.5
  - [ ] Plotly
- [X] PostgreSQL 14
- [X] Docker

## Project Roadmap
#TODO roadmap in projects
## Documentation
#TODO See Github Wiki
## Example of use

### User story 1

### User story 2

# Getting started

## Usage

### Requirements
- Docker
- Make

## Installation
git clone

### Lanuch


## Development
1. Duplicate the .env-example file and rename to ```.env```. Fill in the needed environment variables
2. In the root of the project there are multiple Make commands:
    - ```make up``` --> to start the app
    - ```make stop``` --> to stop the app
    - ```make down``` --> to delete the app (in docker)
    - ```make logs``` --> to view the app activity
    - ```make migrate``` --> to update the database with all the columns
3. When running ```make up``` the app is running on localhost port 8000 --> ```127.0.0.1:8000```
4. Only run ```make migrate``` when new database columns have been created
5. The following commands are only for development
    - ```make makemigrations``` --> to update mirgation files when changes have been made
    - ```make db-redeploy``` --> to reset the database to a previous state. You need a ```database.bak``` in the root of the project, which is a backup of the database. 
    - To get a superuser first run ```make shell``` and then ```pyhton manage.py createsuperuser```

## Contributing

#TODO see contributing.md

### Mindset
### Branching

### Coding guidelines