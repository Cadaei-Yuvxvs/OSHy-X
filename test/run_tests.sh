#!/usr/bin/env bash
set -e 

cp -r . /tmp/OSHy-X

container=$( cat /tmp/OSHy-X/README.md | grep "docker pull" | cut -d " " -f 3 | cut -d "\`" -f 1 )

sudo docker pull $container

sudo docker run -v /tmp/OSHy-X/test:/tmp --entrypoint "python" $container -m pytest /tmp/