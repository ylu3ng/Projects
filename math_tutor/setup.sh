#!/bin/bash
# Setup script for Math Tutor Web App

# Exit on error
set -e

echo "Creating Python venv with system Python..."
/usr/bin/python3 -m venv sysvenv

echo "Activating venv..."
source sysvenv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup complete!"
echo "To activate your environment in the future, run:"
echo "  source sysvenv/bin/activate"

export WOLFRAM_ALPHA_APP_ID="4PL699-V7PYHX5W4K"
export GOOGLE_API_KEY="AIzaSyDJSf15xfex6Ez9cOkUP6ccH2dnsH_ROe4" 
python math_tutor_web.py