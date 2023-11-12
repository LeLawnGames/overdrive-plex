from ODM_Handling.unpack_odms import unpack_and_move
from Chapters_List.chapters import chapters_list
from Chop_Tag_Audio.chop_tag_audio import chop_tag_audio
from XML_JSON.xml_scripts import parse_metadata

def run_script():
    unpack_and_move()
    parse_metadata()
    chapters_list()
    chop_tag_audio()

if __name__ == '__main__':
    run_script()
