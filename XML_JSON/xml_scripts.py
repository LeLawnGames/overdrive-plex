import sys
import os
import shutil
import xml.etree.ElementTree as ET
import json

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from XML_JSON.json_scripts import load_config
from Chapters_List.extract_overdrive_chapters import extract_chapters
from Chapters_List.chapter_ms import add_ms_to_chapters
from XML_JSON.json_scripts import load_config
from Chapters_List.ms_durations import ms_to_durations

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(parent_dir, 'config.json')

config = load_config(config_path)

root_dir = config['annex']

'''Takes the .odm.metadata file and turns it into metadata.xml'''
def rename_xml(subdir, file):
    old_file = os.path.join(subdir, file)
    new_file = os.path.join(subdir, "metadata.xml")
    shutil.copy2(old_file, new_file)

def odm_to_xml(subdir, files):
    for file in files:
        if file.endswith('.odm.metadata'):
            rename_xml(subdir, file)
            break

'''Cleans the metadata'''
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

'''Turns the cleaned xml into a json'''
def xml_to_json(folder_path):
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename == "metadata.xml":
                xml_file = os.path.join(dirpath, filename)
                metadata = extract_metadata(xml_file)
                cleaned_file = os.path.join(dirpath, "cleaned_metadata.json")
                with open(cleaned_file, "w") as f:
                    json.dump(metadata, f)

def parse_metadata():
    for subdir, _, files in os.walk(root_dir):
        odm_to_xml(subdir, files)
    xml_to_json(root_dir)