'''Parses the metadata.xml file into only the required data'''

import os
import xml.etree.ElementTree as ET
import json
from config import annex

def extract_metadata(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = {}
    for child in root:
        '''Finds occurrences of Title, Creators, Subjects and isolates'''
        if child.tag == "Title":
            data["Title"] = child.text
        elif child.tag == "Creators":
            '''Identifies Authors and Narrators'''
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
    #Walks to metadata.xml & exports the parsed version as cleaned_metadata.json
    for dirpath, dirname, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename == "metadata.xml":
                xml_file = os.path.join(dirpath, filename)
                metadata = extract_metadata(xml_file)
                cleaned_file = os.path.join(dirpath, "cleaned_metadata.json")
                with open(cleaned_file, "w") as f:
                    json.dump(metadata, f)
                print(f"Processed {xml_file}, output saved to {cleaned_file}")

path_to_annex = annex
process_folder(path_to_annex)