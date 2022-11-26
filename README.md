# SentiTweet
Interactive dashboard for comprehensive analysis of Twitter tweets

## Project Status
Milestone 1 MUST HAVE

Newest release - none

## Table of Contents
- [SentiTweet](#sentitweet)
  - [Project Status](#project-status)
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
  - [Stories](#stories)
    - [I want to try the app](#i-want-to-try-the-app)
    - [I have found a bug!](#i-have-found-a-bug)
    - [I have a question!](#i-have-a-question)
    - [I want to share my thoughts/ provide feedback!](#i-want-to-share-my-thoughts-provide-feedback)
    - [I want to contribute!](#i-want-to-contribute)
    - [How does the project work?](#how-does-the-project-work)
  - [Usage](#usage)
    - [Requirements](#requirements)
  - [Installation](#installation)
    - [Lanuch](#lanuch)
  - [Development](#development)
  - [Contributing](#contributing)
    - [Mindset](#mindset)
    - [Workflow](#workflow)
    - [Branching](#branching)
    - [Issues labels](#issues-labels)
      - [Labels](#labels)
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

## Stories 

### I want to try the app
There are two options
- online - vist the site
- locally - See #usage

### I have found a bug!
Submit Issue in and label as Bug (it will be solved in next relase), if the bug is breaking add hotfix label instead
### I have a question!
Discussions
### I want to share my thoughts/ provide feedback!
Discussions

### I want to contribute!
See # contribute

### How does the project work?
See wiki for more information

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

### Workflow
1. Create Issue in GitHub
2. Create branch from Issue, it will be auto linked
   
   name the branch ST (for things related to development with sentitweet)

   Example feature/ST-32-name-of-your-issue
3. assign project and set as todo
4. assign yourself
5. add labels
6. assign milestone according to MoSCoV
7. Add subtasks - [ ] 
8. develop
9. make pull request
10. assign reviewer
11. close pull request with comment
   
### Branching
-- `main` branch is protected you cannot directly push to it, because all merges will trigger Github Action that will build and push Container to production


- feature (clearly indicated in roadmap)
- hotfix (on production - directly to main)
- enhacement (visual, improvements)
- bug (on dev, usually spotted when testing, if there is any bug in any branch besides those two should be resolved in the branch there)
- ?docs (readme, wiki)

### Issues labels
Branch classification (assign only one)
- `feature` -> New feature branch
- `style` -> Improvements in visuals or code style
- `enhancement` -> Improvements in existing feature
- `documentation` -> Improvements or additions to documentation (Readme, Wiki)
- `hotfix` -> Critical bug (something isn't working on production)
- `bug` -> Non critical bug (will be fixed in one of the future releases)

Claryfing labels
- `good first issue` -> Good for newcomers
- `help wanted` -> Extra attention is needed

Closing labels - assign and close issue
- `invalid` -> This doesn't seem right
- `wontfix` -> This will not be worked on 
- `duplicate` -> This issue or pull request already exists

#### Labels
Questions should be added in discussions tab, not as an issue



create branch from issue
### Coding guidelines