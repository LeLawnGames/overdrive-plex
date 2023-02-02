#!/bin/bash

#This is a Frankenstein version of chbrowns overdrive script
#
#It extracts the contents of the odm into a temp directory so as to point the metadata
#file to the export path of the contents of the odm and then deletes the leftover files


source config.env
folder=$queue
annex=$annex

for file in $folder/*.odm
do
    #Make temp dir in loop so that it clears even if theres any errors
    temp_dir=$(mktemp -d)
    cd "$temp_dir"

    echo "folder path: $folder"
    echo "temp_dir path: $temp_dir"

    while true; do
        if ~/.local/bin/overdrive download $file; then
            break
        fi
        sleep 2 # wait for 2 seconds before retrying
    done

    #Get the name of the downloaded folder
    downloaded_folder=$(find "$temp_dir" -type d -mindepth 1 -maxdepth 1 | head -n 1)
    echo "downloaded_folder: $downloaded_folder"

    #Move the downloaded folder to the destination
    mv "$downloaded_folder" "$annex"

    #Move the .odm.metadata to the downloaded folder
    metadata_file=$(find "$folder" -name "*.odm.metadata")
    mv "$metadata_file" "$annex/$(basename "$downloaded_folder")"

    #Remove temp directory
    rm -rf "$temp_dir"

done

#Remove .odm & .odm.license files
rm $queue/*.odm
rm $queue/*.odm.license