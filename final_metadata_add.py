#Confirmed working as of 1/23/23

import os
import shutil
import json
import re
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TCOM, TCON, TSOA, TRCK, TIT3, TALB, COMM
from config import circulation,bookshelf

def traverse_directory(directory):
    # Iterate through all subfolders and files
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)
            if os.path.exists(os.path.join(subfolder_path, "cleaned_metadata.json")):
                add_metadata(subfolder_path)

def add_metadata(directory):
    # Get the metadata from the cleaned_metadata.json file in the current subfolder
    with open(os.path.join(directory, "cleaned_metadata.json"), "r") as f:
        json_data = json.load(f)
        artist = json_data.get("Author", "")
        composer = json_data.get("Narrator", "")
        genre = json_data.get("Subjects", "")
        album_title = json_data.get("Title", "")

    # Rest of the code

    # Replace all occurrences of -s with 's in the album title
    album_title = re.sub("-s", "'s", album_title)

    # Get a list of all mp3 files in the current directory
    mp3_files = [f for f in os.listdir(directory) if f.endswith(".mp3")]

    # Sort the list of mp3 files alphabetically
    mp3_files.sort()

    # Iterate through the list of mp3 files
    for i, mp3_file in enumerate(mp3_files, 1):
        mp3_file_path = os.path.join(directory, mp3_file)

        # Extract the title of the mp3 file
        file_name, file_ext = os.path.splitext(mp3_file)
        title = file_name.lstrip("0123456789_")

        # Add the track number to the file using ID3
        audio = ID3(mp3_file_path)
        audio.add(TRCK(encoding=3, text=str(i)))
        audio.add(TIT2(encoding=3, text=title))
        audio.save()

        # Add the metadata to the file using ID3
        audio = ID3(mp3_file_path)
        audio.add(TPE1(encoding=3, text=artist))
        audio.add(TCOM(encoding=3, text=composer))
        audio.add(TCON(encoding=3, text=genre))
        audio.add(TALB(encoding=3, text=album_title))
        audio.save()

        # Check if folder.jpg exists in the current directory
        if os.path.exists(os.path.join(directory, "folder.jpg")):
            # Add the album art to the file using ID3
            with open(os.path.join(directory, "folder.jpg"), "rb") as albumart:
                audio = ID3(mp3_file_path)
                audio.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=albumart.read()))
                audio.save()

# Point the script at a directory
directory = circulation

# Traverse the directory and apply the metadata to the mp3 files
traverse_directory(directory)

for root, dirs, files in os.walk(directory):
    for dir in dirs:
        subfolder_path = os.path.join(root, dir)
        parent_folder = os.path.dirname(subfolder_path)
        if parent_folder == directory:
            shutil.move(subfolder_path, bookshelf)