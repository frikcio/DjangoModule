# E_SHOP
___
This is small instruction to start this project on your local machine
## What do you need:
To start project your local machine must have:
* [docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/install/)
___
## Setup project:
1) Open directory with `docker-compose.yml` and `.env.example` files
2) Rename `.env.example` file as `.env` and change values
3) Open terminal and write commands:
### Common commands:
Build containers:
```commandline
    docker-compose build
```
Apply migrations:
```commandline
    docker-compose run backend python manage.py migrate
```
Run project in console:
```commandline
    docker-compose up
```
or
Run project in background:
```commandline
    docker-compose up -d
```
### Additional commands:
To stop project if it runs in background:
```commandline
    docker-compose stop
```
To down containers:
```commandline
    docker-compose down
```
To down containers and delete database:
```commandline
    docker-compose down --volume
```
For create superuser:
```commandline
    docker-compose run backend python manage.py createsuperuser
```
___
All [docker-compose](https://docs.docker.com/compose/reference/) commands
