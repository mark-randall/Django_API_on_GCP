#!/bin/sh
set -e

if [ "$ENABLE_DB_MIGRATIONS" = true ] ; then

    # Apply database migrations
    echo "Apply database migrations"

    python ./manage.py makemigrations
    python ./manage.py migrate

else
    echo "Migrations disabled set ${ENABLE_DB_MIGRATIONS}=true to enable"
fi