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
    # Make temp dir in loop so that it clears even if there's any errors
    temp_dir=$(mktemp -d)
    cd "$temp_dir"

    echo "folder path: $folder"
    echo "temp_dir path: $temp_dir"

    while true; do
        # Run the overdrive download command and capture both stdout and stderr
        output=$(~/.local/bin/overdrive download "$file" 2>&1)
        exit_status=$?

        # Check if the output contains the specific LicenseError message
        if echo "$output" | grep -q "<ErrorCode>1003</ErrorCode>"; then
            echo "License error detected for file: $file. Redownload the ODM."
            echo "$output"  # Optionally log this output to a file
            break  # Break out of the while loop and skip this file
        elif [ $exit_status -eq 0 ]; then
            echo "Download successful for $file"
            break  # Successful download, break out of the while loop
        else
            echo "An unspecified error occurred, retrying in 2 seconds..."
            sleep 2
        fi
    done

    # Get the name of the downloaded folder
    downloaded_folder=$(find "$temp_dir" -type d -mindepth 1 -maxdepth 1 | head -n 1)
    if [ -n "$downloaded_folder" ]; then
        echo "downloaded_folder: $downloaded_folder"

        # Move the downloaded folder to the destination
        mv "$downloaded_folder" "$annex"

        # Move the .odm.metadata to the downloaded folder
        metadata_file=$(find "$folder" -name "*.odm.metadata")
        if [ -n "$metadata_file" ]; then
            mv "$metadata_file" "$annex/$(basename "$downloaded_folder")"
        fi
    else
        echo "No downloaded folder found for $file, potentially due to earlier license error."
    fi

    # Clean up the temporary directory
    rm -rf "$temp_dir"

done

# Remove .odm & .odm.license files
rm -f $folder/*.odm
rm -f $folder/*.odm.license
