#!/bin/bash

pip install -r ./python-backend/requirements.txt
pip install docker-compose
docker build -t typosquatting-livefeed-backend ./python-backend
docker build -t typosquatting-livefeed-frontend ./web-frontend
docker compose up -d