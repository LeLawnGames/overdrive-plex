import os
import json

def load_config(file_path):
    """Load the JSON config file and return a dictionary."""
    with open(file_path, 'r') as file:
        return json.load(file)
    
def json_to_env(json_file_path):
    with open(json_file_path, 'r') as json_file:
        config = json.load(json_file)
        for key, value in config.items():
            os.environ[key.upper()] = str(value)