#Confirmed working as of 1/22/23

import os

root_dir = '/Users/jonas/Documents/SERVER/BOOKS/TEST'
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        file_path = os.path.join(subdir, file)
        if file == 'overdrive_chapters_ms.txt':
            with open(file_path, "r") as file:
                lines = file.read().split('\n')
            new_file_path = file_path.replace('.txt', '_spans.txt')
            with open(new_file_path, "w") as file:
                for i in range(len(lines)):
                    parts = lines[i].split(" ")
                    if i == len(lines) - 2:
                        # If it's the second-to-last line, write the last line's number and 0
                        file.write(parts[0])
                        file.write("\t" + lines[i + 1].split(" ")[0])
                        file.write("0")
                    elif i != len(lines) - 1:
                        # Otherwise, write the number from the next line to the file
                        file.write(parts[0])
                        file.write("\t" + lines[i + 1].split(" ")[0])
                    else:
                        # If it's the last line, just write the number and 0
                        if parts[0] != "":
                            file.write(parts[0])
                            file.write("0")
                    # Write the rest of the line to the file
                    file.write("\t" + " ".join(parts[1:]))
                    if i != len(lines) - 1 or (i == len(lines) - 1 and lines[i] != ""):
                        file.write("\n")
                if lines[-1] == "":
                    file.seek(file.tell()-1, os.SEEK_SET)
                    file.truncate()