""""
Copyright © antonionardella 2023 - https://github.com/antonionardella (https://antonionardella.it)
Description:
Separated the config to use in it helper functions

Version: 5.5.0
"""
import os
import sys
import json

# Get the path to the current directory
current_directory = os.path.realpath(os.path.dirname(__file__))

# Navigate to the parent directory using '..'
parent_directory = os.path.realpath(os.path.join(current_directory, '..'))

# Check if 'config.json' exists in the parent directory
def load_config(config_file_path):
    config_file_path = os.path.join(parent_directory, 'config.json')
    if not os.path.isfile(config_file_path):
        sys.exit("'config.json' not found in the parent directory! Please add it and try again.")
    else:
        with open(config_file_path) as file:
            return json.load(file)