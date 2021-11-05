#!/bin/sh

# First of all run install.sh
cd "$(dirname "$0")"
source $(pipenv --venv)/bin/activate
python -m unittest discover