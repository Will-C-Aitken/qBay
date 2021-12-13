#!/bin/bash

git fetch
git checkout main
git pull
docker login
docker push cisc327group2/qbay:v1
sudo docker build
sudo docker-compose up
