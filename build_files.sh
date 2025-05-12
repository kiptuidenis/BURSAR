#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python collect_static.py

# Make build_files.sh executable
chmod +x build_files.sh

echo "Build completed successfully"