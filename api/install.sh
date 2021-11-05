#!/bin/sh

cd "$(dirname "$0")"

pip install pipenv
pipenv install --three
pipenv update

chmod +x test.sh
chmod +x dev.sh

./test.sh