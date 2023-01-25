#Confirmed as of 1/22/23

import os
import xml.etree.ElementTree as ET
import json

def extract_metadata(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = {}
    for child in root:
        if child.tag == "Title":
            data["Title"] = child.text
        elif child.tag == "Creators":
            for creator in child:
                if creator.attrib["role"] == "Author":
                    data["Author"] = creator.text
                elif creator.attrib["role"] == "Narrator":
                    data["Narrator"] = creator.text
        elif child.tag == "Subjects":
            subjects = []
            for subject in child:
                subjects.append(subject.text)
            data["Subjects"] = ", ".join(subjects)
    return data

def process_folder(folder_path):
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename == "metadata.xml":
                xml_file = os.path.join(dirpath, filename)
                metadata = extract_metadata(xml_file)
                cleaned_file = os.path.join(dirpath, "cleaned_metadata.json")
                with open(cleaned_file, "w") as f:
                    json.dump(metadata, f)
                print(f"Processed {xml_file}, output saved to {cleaned_file}")

folder_path = "/Users/jonas/Documents/SERVER/BOOKS/TEST"
process_folder(folder_path)