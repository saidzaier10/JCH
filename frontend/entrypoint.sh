#!/bin/sh

# Install dependencies
echo "Installing frontend dependencies..."
npm install

# Execute the main command
exec "$@"
