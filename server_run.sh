#!/bin/bash

cd ./backend

#spwan the containers with docker-compose

sudo docker-compose build

#run the containers

sudo docker-compose up
