#!/bin/sh
set -e

# Apply database migrations
echo "Apply database migrations"
python ./manage.py makemigrations
python ./manage.py migrate