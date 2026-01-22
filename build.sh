#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Tailwind dependencies
# This command uses the NPM_BIN_PATH you set in settings
python manage.py tailwind install --no-package-lock

# Build the production CSS
python manage.py tailwind build

# Standard Django deployment steps
python manage.py collectstatic --no-input
python manage.py migrate