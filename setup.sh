#!/bin/bash

pip install --upgrade -r ./requirements.txt
pip install docker-compose
docker image pull -a gatheringrays/typosquatting-livefeed
chmod +700 ./start.sh
