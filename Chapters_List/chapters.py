import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from Chapters_List.extract_overdrive_chapters import extract_chapters
from Chapters_List.chapter_ms import add_ms_to_chapters
from XML_JSON.json_scripts import load_config
from Chapters_List.ms_durations import ms_to_durations

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(parent_dir, 'config.json')

config = load_config(config_path)

queue = config['queue'] #Where your ODMs are downloaded to
annex = config['annex'] #Where the ODMs get unpackaged to
circulation = config['circulation'] #Where the chapterized mp3s get saved
bookshelf = config['bookshelf'] #Where the final audiobook gets dropped

def chapters_list():
    extract_chapters(annex)
    add_ms_to_chapters(annex)
    ms_to_durations(annex)
    print("Splitting audio files into chapters & adding metadata (this may take a moment)...")

if __name__ == '__main__':
    chapters_list()