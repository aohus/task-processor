#!/bin/bash
python3.9 -m venv $1
source $1/bin/activate
pip install --upgrade pip
pip install -I -U -r ./requirements.txt
