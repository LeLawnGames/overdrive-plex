#!/bin/bash

#download odm's to chosen directory

# configure variables
python3.10 config.py

# unpack odm's
#bash overdrivedelete.sh

# extract chapters, specify folder holding the unpackaged overdrive mp3's
##source config.env
#python3 extract_overdrive_chapters.py $annex

# clean metadata
#python3 metadatatoxml.py

##python3 xmlparse.py

# turn chapters into ms
#python3 chapter_ms.py

# format durations
#python3 durations.py

# export labeled audio and archive original folder 
# FIX: MAKE SURE IT CAN ADD TO EXISTING AUTHOR FOLDER
python3 00_exportchapters.py

# tag the exported audio with proper metadata
python3 final_metadata_add.py

#manually add to Plex
