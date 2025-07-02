#!/bin/bash

# Navigate to the directory containing the script
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Install required packages
if [  -f "requirements.txt" ]; then
  echo "Installing required packages..."
  pip install -r requirements.txt
else
  echo "requirements.txt not found. Skipping package installation."
fi


# Run the Python script
py backend/import_cat_facts.py