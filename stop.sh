#!/bin/bash

# this assumes docker is running and docker-compose is installed

compose_file="compose-nerfball.yml"

echo "Stopping nerfball with compose_file=${compose_file}"
docker-compose -f ${compose_file} stop

if [[ "$?" == "0" ]]; then
    docker rm nerfball >> /dev/null 2>&1
fi

exit 0
