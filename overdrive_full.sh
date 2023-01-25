#!/bin/bash

#download odm's to chosen directory

#navigate to folder where scripts are located

cd /Users/jonas/Documents/code/overdrive-plex

# unpack odm's
bash overdrivedelete.sh

# extract chapters
python3.10 extract_overdrive_chapters.py /Users/jonas/Documents/SERVER/BOOKS/01_ANNEX

# clean metadata
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
