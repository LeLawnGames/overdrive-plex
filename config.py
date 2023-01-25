# Define directories
# I like having multiple folders so as to visualize each step happening
# but you could easily adjust the setup to fit your preferences

import os

# Where you will be downloading your .odm's to, we're writing this one
# as an environment for the bash to reference
os.environ["queue"] = "/Users/jonas/Documents/SERVER/QUEUE"

# Where the unpackaged odm mp3s will get moved
# First for the bash
os.environ["annex"] = "/Users/jonas/Documents/SERVER/BOOKS/01_ANNEX"
# Then for python
annex="/Users/jonas/Documents/SERVER/BOOKS/01_ANNEX"

# Where chapterized and labeled mp3s will be stored
circulation="/Users/jonas/Documents/SERVER/BOOKS/02_CIRCULATION"

# Where the final finished product will land
bookshelf="/Users/jonas/Documents/SERVER/BOOKS/03_READY_FOR_PLEX"

# Where the scraps go
archive="/Users/jonas/Documents/SERVER/BOOKS/00_ARCHIVE"