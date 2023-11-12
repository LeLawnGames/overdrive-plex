'''Converts label durations to milliseconds for pydub to read'''
import os
import re
from datetime import datetime, timedelta

def duration_to_milliseconds(duration):
    '''Conversion from Seconds to Milliseconds'''
    hours, minutes, seconds = duration.split(':')
    seconds = int(hours)*3600 + int(minutes)*60 + float(seconds)
    return int(seconds * 1000)

def read_chapters_file(dirpath, filename):
    '''Open the chapters file and read the contents.'''
    with open(os.path.join(dirpath, filename), 'r') as f:
        lines = f.readlines()
    return lines

def new_file(dirpath, filename):
    '''Create a new file with the same name but with "ms" added to the end.'''
    lines = read_chapters_file(dirpath, filename)
    new_filename = filename[:-4] + "_ms.txt"
    with open(os.path.join(dirpath, new_filename), 'w') as new_file:
        for line in lines:
            duration, label = re.split(r"\s+", line.strip(), 1)
            milliseconds = duration_to_milliseconds(duration)
            new_file.write(f'{milliseconds} {label}\n')

def add_ms_to_chapters(directory):
    '''Loop through all files in the directory tree and process the matching files.'''
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith("overdrive_chapters") and filename.endswith(".txt"):
                new_file(dirpath, filename)