#!/bin/bash

git fetch
git checkout main
git pull
sudo docker build
sudo docker-compose up
