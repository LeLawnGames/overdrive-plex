#!/bin/bash

#download odm's

# NOTE: The odm's come with metadata -- for the future system use that file because it's more reliable.

# navigate to the folder where the first script is located
cd /Users/jonas/Documents/SERVER/FRAMEWORK

# unpack odm's
bash overdrivedelete.sh

# navigate to the folder where the second script is located
cd /Users/jonas/Documents/SERVER/BOOKS/TEST

# extract chapters
python3.10 extract_overdrive_chapters.py /Users/jonas/Documents/SERVER/BOOKS/01_ANNEX

# navigate back to the directory where the shell script is located
cd /Users/jonas/Documents/SERVER/LOCKED_CODE

# clean metadata
#python3.10 00_format_metadata.py
python3.10 metadatatoxml.py

python3.10 xmlparse.py

# turn chapters into ms
python3.10 chapter_ms.py

# format durations
python3.10 durations.py

# export labeled audio and archive original folder 
# FIX: MAKE SURE IT CAN ADD TO EXISTING AUTHOR FOLDER
python3.10 00_exportchapters.py

# tag the exported audio with proper metadata
python3.10 final_metadata_add.py

#manually add to Plex
