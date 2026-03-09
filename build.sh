#!/usr/bin/env bash
# Exit on error
set -o errexit

# Check Python version (for debugging)
python --version

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input --clear

