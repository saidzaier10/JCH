#!/bin/sh

# Install dependencies
echo "Installing backend dependencies..."
pip install --no-cache-dir -r requirements.txt

# Run migrations
python manage.py migrate

# Execute the main command
exec "$@"
