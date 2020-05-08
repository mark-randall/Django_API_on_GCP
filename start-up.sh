#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
#python ./manage.py syncdb
python ./manage.py migrate
python ./manage.py makemigrations