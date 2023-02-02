
'''Takes the .odm.metadata file and turns it into metadata.xml'''

import os
import shutil
from config import annex

root_dir = annex

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.odm.metadata'):
            old_file = os.path.join(subdir, file)
            new_file = os.path.join(subdir, "metadata.xml")
            shutil.copy2(old_file, new_file)
            break
