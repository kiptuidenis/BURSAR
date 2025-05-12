#!/bin/bash

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Copy static files
if [ -d "app/static" ]; then
  cp -r app/static/* staticfiles/
else
  echo "No static directory found"
  # Create a placeholder file to ensure the directory isn't empty
  echo "<html><body>Static files will be served here</body></html>" > staticfiles/index.html
fi

echo "Static files collection complete"

echo "Build completed successfully"