import sys
import os
import subprocess

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from XML_JSON.json_scripts import json_to_env
from XML_JSON.json_scripts import load_config

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(parent_dir, 'config.json')

config = load_config(config_path)

BASH_SCRIPT_PATH = './ODM_Handling/overdrivedelete.sh'

def run_chbrown_overdrive(bash_script_path):
    subprocess.run(['chmod', '+x', bash_script_path]) #Make overdrivedelete.sh executable
    subprocess.run(bash_script_path, shell=True, executable='/bin/bash', env=os.environ)

def unpack_and_move():
    # Load the configuration from JSON into environment variables
    json_to_env(config_path)
    
    # Run the Bash script
    run_chbrown_overdrive(BASH_SCRIPT_PATH)