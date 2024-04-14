#!/bin/bash

pip install -r ./python-backend/requirements.txt
pip install docker-compose
docker image pull -a gatheringrays/typosquatting-livefeed
chmod +700 ./start.sh
