#Confirmed working as of 1/22/23

import os
import shutil
from pydub import AudioSegment
from config import annex,circulation,archive

AudioSegment.converter = "/opt/homebrew/Cellar/ffmpeg/5.1.2_3/bin/ffmpeg"
AudioSegment.ffmpeg = "/opt/homebrew/Cellar/ffmpeg/5.1.2_3/bin/ffmpeg"
AudioSegment.ffprobe ="/opt/homebrew/Cellar/ffmpeg/5.1.2_3/bin/ffmpeg"

def export_audio_file(start, end, name):
    start_ms = int(start)
    end_ms = int(end)
    export = combined[start_ms:end_ms]
    folder_name = folder.split(" - ")[-1].strip()
    destination_path = circulation
    author_name = folder.split(" - ")[0].strip()
    export_folder = os.path.join(destination_path, author_name, folder_name)
    author_folder = os.path.join(destination_path, author_name)
    if not os.path.exists(author_folder):
        os.makedirs(author_folder)
        export_folder = os.path.join(author_folder, folder_name)

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    export_path = os.path.join(export_folder, f"{name}.mp3")
    export.export(export_path, format="mp3")

    metadata_file = os.path.join(folder_path, "cleaned_metadata.json")
    chapters_file = os.path.join(folder_path, "overdrive_chapters_ms.txt")
    album_art = os.path.join(folder_path, "folder.jpg")
    if os.path.exists(album_art):
        shutil.copy(album_art, export_folder)
    shutil.copy(metadata_file, export_folder)

main_directory = annex

for folder in sorted(os.listdir(main_directory)):
    folder_path = os.path.join(main_directory, folder)
    if os.path.isdir(folder_path):
        try:
            # Import MP3s in alphabetical order
            mp3_files = sorted(os.listdir(folder_path))
            mp3_files = [os.path.join(folder_path, file) for file in mp3_files if file.endswith(".mp3")]
            
            combined = AudioSegment.empty()
            for mp3_file in mp3_files:
                print(mp3_file)
                combined += AudioSegment.from_file(mp3_file)

            # Align end to end
            combined = combined.set_channels(1)

            # Import labels
            labels_file = os.path.join(folder_path, "overdrive_chapters_ms_spans.txt")
            labels = []
            with open(labels_file, "r") as f:
                for line in f:
                    start, end, name = line.strip().split("\t")
                    labels.append((start, end, name))

            # Initialize counter for duplicate label names
            counter = {}

            # Initialize counter for file export
            file_count = 0

            for i, label in enumerate(labels):
                start, end, name = label
                if end == "0" and i == len(labels) - 1:
                    end = combined.duration_seconds * 1000

                file_count += 1
                name = f"{file_count:03}_{name.replace('/', '_')}" 
                # format file_count as 3 digit number
                export_audio_file(start, end, name)

        except Exception as e:
            print(f"Error processing {folder}: {e}")
    
    #Archive everything except chapters_list.py
    if folder_path != "chapters_list.py":
        shutil.move(folder_path, archive/ + folder)