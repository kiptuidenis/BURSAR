#!/bin/bash
set -e

echo "Starting build process..."

# Create required directories
mkdir -p staticfiles
mkdir -p public

# Install Python dependencies
pip install -r requirements.txt

# Run static file collection using Python script
python collect_static.py

# Create a backup of index.html in staticfiles for fallback
cp public/index.html staticfiles/index.html 2>/dev/null || echo "No public/index.html to copy"

echo "Build completed successfully"