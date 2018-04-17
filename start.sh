#!/bin/bash

# this assumes docker is running and docker-compose is installed

compose_file="compose-nerfball.yml"

echo "Starting nerfball with compose_file=${compose_file}"
docker-compose -f $compose_file up -d

exit 0
