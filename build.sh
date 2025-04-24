#!/usr/bin/env bash

echo "Collecting static files..."
python manage.py collectstatic --noinput
