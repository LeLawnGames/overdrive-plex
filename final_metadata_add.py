'''Adds metadata to the chapterized mp3s'''

import os
import shutil
import json
import re
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TCOM, TCON, TRCK, TALB
from config import circulation,bookshelf

def traverse_directory(directory):
    '''Iterate through all subfolders & create cleaned_metadata.json'''
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)
            metadata_file = os.path.join(subfolder_path, "cleaned_metadata.json")
            if os.path.exists(metadata_file):
                metadata = read_metadata(metadata_file)
                if metadata is None:
                    print("Skipping due to json error")
                    continue
                add_metadata_to_files(subfolder_path, metadata)

def read_metadata(metadata_file):
    '''Read and return json data from the given metadata file'''
    try:
        with open(metadata_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading metadata file {metadata_file}: {e}")
        return None

def get_album_title(metadata):
    '''Extract the Book Title from metadata and clean it'''
    album_title = metadata.get("Title", "")
    return re.sub(r"-s\b", "'s", album_title)

def get_artist(metadata):
    '''Extract the Author from metadata'''
    return metadata.get("Author", "")

def get_composer(metadata):
    '''Extract the Narrator from metadata'''
    return metadata.get("Narrator", "")

def get_genre(metadata):
    '''Extract the Subjects from metadata'''
    return metadata.get("Subjects", "")

def add_metadata_to_files(directory, metadata):
    '''Add metadata to all chapterized mp3s in the directory'''
    album_title = get_album_title(metadata)
    artist = get_artist(metadata)
    composer = get_composer(metadata)
    genre = get_genre(metadata)

    '''Get a list of all mp3 files in the current directory'''
    mp3_files = [f for f in os.listdir(directory) if f.endswith(".mp3")]

    '''Sort the list of mp3 files alphabetically'''
    mp3_files.sort()

    '''Iterate through the list of mp3 files'''
    for i, mp3_file in enumerate(mp3_files, 1):
        mp3_file_path = os.path.join(directory, mp3_file)

        '''Extract the title of the mp3 file'''
        file_name = os.path.splitext(mp3_file)
        title = file_name.lstrip("0123456789_")

        '''Add the track number to the file using ID3'''
        audio = ID3(mp3_file_path)
        audio.add(TRCK(encoding=3, text=str(i)))
        audio.add(TIT2(encoding=3, text=title))
        audio.save()

        '''Add the metadata to the file using ID3'''
        audio = ID3(mp3_file_path)
        audio.add(TPE1(encoding=3, text=artist))
        audio.add(TCOM(encoding=3, text=composer))
        audio.add(TCON(encoding=3, text=genre))
        audio.add(TALB(encoding=3, text=album_title))
        audio.save()

        '''Check if folder.jpg exists in the current directory'''
        if os.path.exists(os.path.join(directory, "folder.jpg")):
            '''Add the album art to the file using ID3'''
            with open(os.path.join(directory, "folder.jpg"), "rb") as albumart:
                audio = ID3(mp3_file_path)
                audio.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=albumart.read()))
                audio.save()

'''Point the script at your Circulation folder'''
directory = circulation

traverse_directory(directory)

for root, dirs, files in os.walk(directory):
    '''Traverse the directory and apply the metadata to the mp3 files'''
    for dir in dirs:
        subfolder_path = os.path.join(root, dir)
        parent_folder = os.path.dirname(subfolder_path)
        if parent_folder == directory:
            shutil.move(subfolder_path, bookshelf)