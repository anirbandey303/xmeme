#!/bin/bash

sudo apt-get update

#install docker

sudo apt --yes install docker.io

sudo systemctl enable --now docker

sudo apt --yes install docker-compose
