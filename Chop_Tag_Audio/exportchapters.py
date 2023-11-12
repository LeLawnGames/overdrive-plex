import os
import shutil
from pydub import AudioSegment
from XML_JSON.json_scripts import load_config
from Chop_Tag_Audio.progress_bar import process_progress, get_chapter_count

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(parent_dir, 'config.json')
config = load_config(config_path)

path_to_ffmpeg = config['ffmpeg']
archive = config['archive']
annex = config['annex']
circulation = config['circulation']

AudioSegment.converter = path_to_ffmpeg
AudioSegment.ffmpeg = path_to_ffmpeg
AudioSegment.ffprobe = path_to_ffmpeg

def export_audio_file(combined, start_ms, end_ms, name, circulation, author_name, folder_name):
    export = combined[start_ms:end_ms]
    export_folder = os.path.join(circulation, author_name, folder_name)
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    export_path = os.path.join(export_folder, f"{name}.mp3")
    export.export(export_path, format="mp3")
    return export_folder  # Return the folder path where the file was exported

def split_mp3s(annex, circulation):
    total_chapters = get_chapter_count(annex)
    overall_progress_bar = process_progress(total_chapters)

    for folder in sorted(os.listdir(annex)):
        folder_path = os.path.join(annex, folder)
        if os.path.isdir(folder_path):
            file_count = 0  # Reset file_count to 0 for each new folder
            try:
                mp3_files = [file for file in sorted(os.listdir(folder_path)) if file.endswith(".mp3")]
                combined = AudioSegment.empty()
                for mp3_file in mp3_files:
                    combined += AudioSegment.from_file(os.path.join(folder_path, mp3_file))
                combined = combined.set_channels(1)  # Assuming you want mono audio

                labels_file = os.path.join(folder_path, "overdrive_chapters_ms_spans.txt")
                with open(labels_file, "r") as f:
                    labels = [line.strip().split("\t") for line in f]

                for start, end, name in labels:
                    if end == "0":
                        end = str(len(combined))  # Use str to keep it consistent with start
                    start_ms = int(start)
                    end_ms = int(end)
                    author_name, folder_name = folder.split(" - ")
                    formatted_name = f"{file_count:03}_{name.replace('/', '_')}"  # Formatting name with file_count

                    export_folder = export_audio_file(combined, start_ms, end_ms, formatted_name, circulation, author_name.strip(), folder_name.strip())
                    artwork_and_metadata(export_folder, folder_path)

                    overall_progress_bar.update(1)

                    file_count += 1  # Increment file_count after each file is exported
                
            except Exception as e:
                print(f"Error processing {folder}: {e}")

            archive_folder = os.path.join(archive, folder)
            if not os.path.exists(archive_folder):
                os.makedirs(archive_folder)
            shutil.move(folder_path, archive_folder)

def artwork_and_metadata(export_folder, folder_path):
    metadata_file = os.path.join(folder_path, "cleaned_metadata.json")
    album_art = os.path.join(folder_path, "folder.jpg")
    if os.path.exists(album_art):
        shutil.copy(album_art, export_folder)
    if os.path.exists(metadata_file):
        shutil.copy(metadata_file, export_folder)

if __name__ == '__main__':
    split_mp3s(annex, circulation)
