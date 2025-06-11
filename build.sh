#!/bin/bash

apt-get update && apt-get install -y python3-dev libxml2-dev libxslt-dev libjpeg-dev zlib1g-dev libffi-dev libssl-dev
pip install --upgrade pip
pip install -r requirements.txt
