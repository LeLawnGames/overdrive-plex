#This officially works for the full ODM extraction as of 1/21/23 at 9:54pm

# Define the directories
source config.env
input_folder=$queue
output_folder=$annex

shopt -s nullglob
if [ -z "$(find $input_folder -type f -name '*.odm')" ]; then
  echo "No .odm files found in $input_folder, exiting."
  exit 0
fi

# Open ODM's in temporary directory and export contents
for file in $input_folder/*.odm
do
    # Make temp dir in loop so that it clears even if there's any errors
    temp_dir=$(mktemp -d)
    cd "$temp_dir"

    echo "folder path: $input_folder"
    echo "temp_dir path: $temp_dir"

    while true; do
        if ~/.local/bin/overdrive download $file; then
            break
        fi
        sleep 2 # wait for 2 seconds before retrying
    done

    # Get the name of the downloaded folder
    downloaded_folder=$(find "$temp_dir" -type d -mindepth 1 -maxdepth 1 | head -n 1)
    echo "downloaded_folder: $downloaded_folder"

    # Move the downloaded folder to the destination
    mv "$downloaded_folder" "$output_folder"

    # Move the .odm.metadata to the downloaded folder
    metadata_file=$(find "$input_folder" -name "*.odm.metadata")
    mv "$metadata_file" "$output_folder/$(basename "$downloaded_folder")"

    # Delete leftover .odm and .odm.license files
    odm=$(find "$input_folder" -name "*.odm")
    license=$(find "$input_folder" -name "*.odm.license")
    rm $odm
    rm $license

    rm -rf "$temp_dir"
done