# SentiTweet
Interactive dashboard for comprehensive analysis of Twitter tweets

## Table of Contents
- [SentiTweet](#sentitweet)
  - [Table of Contents](#table-of-contents)
- [About](#about)
  - [Motivation](#motivation)
  - [Features](#features)
  - [Technologies](#technologies)
  - [Roadmap](#roadmap)
  - [Examples of use](#examples-of-use)
    - [User story 1](#user-story-1)
    - [User story 2](#user-story-2)
- [Getting started](#getting-started)
  - [Stories](#stories)
    - [I want to use the app! :D](#i-want-to-use-the-app-d)
    - [I have found a bug!](#i-have-found-a-bug)
    - [I have a question!](#i-have-a-question)
    - [I want to share my idea / request new feature!](#i-want-to-share-my-idea--request-new-feature)
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
      - [Todo stage](#todo-stage)
      - [In progress stage](#in-progress-stage)
      - [Done stage](#done-stage)
    - [Branching](#branching)
      - [Naming convention](#naming-convention)
    - [Issues](#issues)
      - [Labels](#labels)
    - [Coding guidelines](#coding-guidelines)
- [Documentation](#documentation)


# About

## Motivation
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

## Roadmap
See [Projects tab](https://github.com/SentiStock/SentiTweet/projects?query=is%3Aopen?type=new&query=is:open%20sort:updated-asc) to view Kanban boards with current development progress

## Examples of use

### User story 1

### User story 2

# Getting started

## Stories 

### I want to use the app! :D
You can either use it:
- online - vist [this site]()
- locally - read [usage](#usage)

### I have found a bug!
Create an Issue in GitHub and label it as:
- bug -> if it is casual
- hotfix -> if it is critical

### I have a question!
Go to [Q&A thread in Discussions tab](https://github.com/SentiStock/SentiTweet/discussions/categories/q-a) and ask us anything! We are always willing to answer :D
### I want to share my idea / request new feature!
Go to [Ideas thread in Discussions tab](https://github.com/SentiStock/SentiTweet/discussions/categories/ideas) and explain your idea, maybe we will include it in a future release!

### I want to contribute!
Read [Contributing guidelines]()

### How does the project work?
See [Documentation]() for comprehensive information

## Usage

### Requirements
- Docker
- Make

## Installation
There are 3 ways to download the repository:
- zip file (not recommended)
- https (most common)
- ssh (recommended)

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
Work in a way that anyone could take the work after you and progess with it further.

### Workflow

#### Todo stage
1. Create Issue on GitHub and name it concisely (it will be also the name of the branch!)
2. Break the task into multiple subtasks by adding "- [ ]" to the description of the issue
3. Classify the issue as [`bug`, `feature`, `documentation`, `style`, `enhacement`] by assigning appropriate label (only one!). If confused see [labels taxonomy](#labels).
4.  Assign issue to milestone (Must have, Should have, Could have, Won't have this time)
5. Assign issue to project name as the priority you chose in previous step
   
#### In progress stage
1. Assign yourself to the issue
2. Create new branch from Issue using development section in the right sidebar (it will allow automated workflows)
3. Name the branch accoriding to [naming convention](#naming-convention) and class you chose in step 2. Example: `feature/ST-32-name-of-your-issue`
4. Checkout on the branch and do the work

#### Done stage
1.  Make pull request to the DEV branch
2.  Assign reviewer
3.  Close pull request with comment (it will automatically close the issue and projects as Done)
   
### Branching
-- `main` branch is protected you cannot directly push to it, because all merges will trigger Github Action that will build and push Container to production

#### Naming convention
\<class-of-branch>/ST-\<issue-number>-\<issue-name>

Examples: 
- `feature/ST-31-core-dashboard`
- `hotfix/ST-52-logout-button-not-working`
- `bug/ST-147-dark-theme-not-not-applied-to-sidebar`

### Issues

#### Labels
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
### Coding guidelines

# Documentation
See [Github Wiki](https://github.com/SentiStock/SentiTweet/wiki)