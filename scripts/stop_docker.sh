#!/bin/bash

if [ "$(docker ps -aq)" ]; then
    docker stop $(docker ps -aq)
    docker rm $(docker ps -aq)
fi
