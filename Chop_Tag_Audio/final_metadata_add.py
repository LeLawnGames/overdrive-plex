'''Adds metadata to the chapterized mp3s'''

import os
import shutil
import json
import re
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TCOM, TCON, TRCK, TALB, ID3NoHeaderError

def process_directories(directory):
    '''Iterate through all subfolders in each author's directory & create cleaned_metadata.json'''
    for author_name in os.listdir(directory): 
        author_path = os.path.join(directory, author_name)
        if os.path.isdir(author_path): 
            for book_title in os.listdir(author_path):
                if book_title == '.DS_Store':  # Skip .DS_Store files/folders at this level, update for your systems specs
                    continue
                book_path = os.path.join(author_path, book_title)
                metadata_file = os.path.join(book_path, "cleaned_metadata.json")
                if os.path.exists(metadata_file):
                    metadata = read_metadata(metadata_file)
                    if metadata:
                        add_metadata_to_files(book_path, metadata)
                    else:
                        print(f"Skipping {book_title} due to json error")
                else:
                    print(f"Metadata file not found in {book_title}")

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
    if not metadata:
        print(f"No metadata available for directory {directory}. Skipping.")
        return
    album_title_1 = get_album_title(metadata)
    artist = get_artist(metadata)
    composer = get_composer(metadata)
    genre = get_genre(metadata)

    '''Replace all occurrences of -s with "'s" in the album title'''
    album_title_2 = re.sub("-s", "'s", album_title_1)
    '''Replace all remaining occurrences of - with "'" in the album title'''
    album_title = re.sub("-", "'", album_title_2)

    '''Get a list of all mp3 files in the current directory'''
    mp3_files = [f for f in os.listdir(directory) if f.endswith(".mp3")]

    '''Sort the list of mp3 files alphabetically'''
    mp3_files.sort()

    '''Iterate through the list of mp3 files'''
    for i, mp3_file in enumerate(mp3_files, 1):
        mp3_file_path = os.path.join(directory, mp3_file)

        '''Extract the title of the mp3 file'''
        file_name, _ = os.path.splitext(mp3_file)
        title = re.sub(r"^\d+_", "", file_name)  # Correctly extracts the title from the filename

        '''Add the track number & other metadata to the file using ID3'''
        try:
            audio = ID3(mp3_file_path)
        except ID3NoHeaderError:
            audio = ID3()

        audio.add(TRCK(encoding=3, text=str(i)))
        audio.add(TIT2(encoding=3, text=title))
        audio.add(TPE1(encoding=3, text=artist))
        audio.add(TCOM(encoding=3, text=composer))
        audio.add(TCON(encoding=3, text=genre))
        audio.add(TALB(encoding=3, text=album_title))
        '''Check if folder.jpg exists in the current directory'''
        album_art_path = os.path.join(directory, "folder.jpg")
        if os.path.exists(album_art_path):
            '''Add the album art to the file using ID3'''
            with open(album_art_path, "rb") as albumart:
                audio.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=albumart.read()))
        
        audio.save(mp3_file_path)  # Save the tags to the file

def meta_to_mp3(directory, bookshelf):
    for author_name in os.listdir(directory):
        author_path = os.path.join(directory, author_name)
        if os.path.isdir(author_path):
            for book_title in os.listdir(author_path):
                if book_title == '.DS_Store':  # Skip .DS_Store files/folders at this level
                    continue
                book_path = os.path.join(author_path, book_title)
                destination_path = os.path.join(bookshelf, author_name, book_title)
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.move(book_path, destination_path)
                print(f"Completed: '{book_title}' by '{author_name}'")
            # After moving all books, check if the author directory is empty and remove it
            if not os.listdir(author_path):
                os.rmdir(author_path)

def traverse_directory(directory, bookshelf):
    process_directories(directory)
    meta_to_mp3(directory, bookshelf)