'''Converts label durations to milliseconds for pydub to read'''

import os
import re
from datetime import datetime, timedelta
from config import annex

def duration_to_milliseconds(duration):
    '''Conversion from Seconds to Milliseconds'''
    hours, minutes, seconds = duration.split(':')
    seconds = int(hours)*3600 + int(minutes)*60 + float(seconds)
    return int(seconds * 1000)

'''path to directory containing the files'''
directory = annex

'''loop through all files in directory tree'''
for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if filename.startswith("overdrive_chapters") and filename.endswith(".txt"):
            '''open the chapters file and read the contents'''
            with open(os.path.join(dirpath, filename), 'r') as f:
                lines = f.readlines()

            '''create a new file with the same name but with "ms" added to the end'''
            new_filename = filename[:-4] + "_ms.txt"
            with open(os.path.join(dirpath, new_filename), 'w') as new_file:
                '''loop through each line in the file'''
                for line in lines:
                    '''split the line into duration and label name using regular expression'''
                    duration, label = re.split(r"\s+", line.strip(), 1)
                    '''convert the duration to milliseconds'''
                    milliseconds = duration_to_milliseconds(duration)
                    '''write the converted duration and label to the new file'''
                    new_file.write(f'{milliseconds} {label}\n')
