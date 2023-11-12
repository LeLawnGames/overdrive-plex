'''Align tracks end to end, chop based on chapters list durations, export to final folder, archive originals'''
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from XML_JSON.json_scripts import load_config
from Chop_Tag_Audio.final_metadata_add import traverse_directory
from Chop_Tag_Audio.exportchapters import split_mp3s

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(parent_dir, 'config.json')

config = load_config(config_path)

path_to_ffmpeg = config['ffmpeg']
archive = config['archive']
annex = config['annex']
circulation = config['circulation']
bookshelf = config['bookshelf']

def chop_tag_audio():
    split_mp3s(annex, circulation)
    traverse_directory(circulation, bookshelf)

if __name__ == '__main__':
    chop_tag_audio()