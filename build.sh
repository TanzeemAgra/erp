#!/bin/bash

# Install setuptools first to ensure pkg_resources is available
pip install --upgrade pip
pip install setuptools==69.0.0
pip install wheel

# Then install all other requirements
pip install -r backend/requirements.txt

# Run Django setup
cd backend
python manage.py collectstatic --noinput
python manage.py migrate --noinput
