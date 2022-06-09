#!/bin/bash

pip install pytest

python -m pip install --upgrade pip
pip install -r tmp/requirements.txt
python -m pytest /OSHy