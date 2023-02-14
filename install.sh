#!/bin/sh
# Bash script to install python 3.9 if it is not already installed.
# Then install virtualenv if not already installed.
# Then create a virtual environment for the project.
# Then install the python requirements for the project.
# The installations should work on mac and linux.

# Install python 3.9 if not already installed
echo "Installing python 3.9 if not already installed..."
# If mac
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install python@3.9
# If linux
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get install python3.9
fi

# Install virtualenv if not already installed
echo "Installing virtualenv if not already installed..."
# If mac
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install virtualenv
# If linux
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get install virtualenv
fi

# Create a virtual environment for the project
echo "Creating a virtual environment for the project..."
virtualenv -p python3.9 venv

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Install the python requirements
echo "Installing the python requirements..."
cd src
pip install -r requirements-test.txt
