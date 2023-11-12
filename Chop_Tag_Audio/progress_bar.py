import sys
import os
import fnmatch
from tqdm import tqdm

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from XML_JSON.json_scripts import load_config

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(parent_dir, 'config.json')

config = load_config(config_path)

directory = config['circulation']

def get_chapter_count(directory):
    total_chapters = 0
    for root, _, files in os.walk(directory):
        for filename in fnmatch.filter(files, 'overdrive_chapters_ms_spans.txt'):
            file_path = os.path.join(root, filename)
            with open(file_path, 'r') as f:
                total_chapters += sum(1 for _ in f)
    return total_chapters

def process_progress(total_chapters):
    return tqdm(total=total_chapters, ncols=75, desc="Splitting mp3's...")