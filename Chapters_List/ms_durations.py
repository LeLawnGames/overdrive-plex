'''Takes the contents of the Milliseconds durations/labels file and creates start/end times'''
import os

def create_durations(file, lines):
    for i in range(len(lines)):
        parts = lines[i].split(" ")
        if i == len(lines) - 2:
            '''If it's the second-to-last line, write the last line's number and 0'''
            file.write(parts[0])
            file.write("\t" + lines[i + 1].split(" ")[0])
            file.write("0")
        elif i != len(lines) - 1:
            '''Otherwise, write the number from the next line to the file'''
            file.write(parts[0])
            file.write("\t" + lines[i + 1].split(" ")[0])
        else:
            '''If it's the last line, just write the number and 0'''
            if parts[0] != "":
                file.write(parts[0])
                file.write("0")
        '''Write the rest of the line to the file'''
        file.write("\t" + " ".join(parts[1:]))
        if i != len(lines) - 1 or (i == len(lines) - 1 and lines[i] != ""):
            file.write("\n")

def bookmark_final_duration(file, lines):
    if lines[-1] == "":
                    '''Ensures there's no empty line at the end of the txt'''
                    file.seek(file.tell()-1, os.SEEK_SET)
                    file.truncate()

def create_spans_txt(file, file_path):
     if file == 'overdrive_chapters_ms.txt':
            with open(file_path, "r") as file:
                lines = file.read().split('\n')
            new_file_path = file_path.replace('.txt', '_spans.txt')
            with open(new_file_path, "w") as file:
                 create_durations(file, lines)
                 bookmark_final_duration(file, lines)

def ms_to_durations(directory):
    for subdir, _, files in os.walk(directory):
        for file in files:
            '''Locates "overdrive_chapters_ms.txt"'''
            file_path = os.path.join(subdir, file)
            create_spans_txt(file, file_path)