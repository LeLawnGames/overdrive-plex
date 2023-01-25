# overdrive-plex
Automates the process of opening Overdrive .odm files and formatting them for use in Plex including editing down to chapters and adding metadata on Mac OS.

See the end of this readme for a long list of credits as this code is based on many pre-existing projects and scripts and would fully not be possible without them.

The simple goal here is to make the process of unpacking and editing .odm files a lot simpler. The issue I have run into is that Overdrive provides mp3 files split up into parts, but those parts don't align with chapters and the only real solution I've found out there is to use Audacity to manually label each chapter. I did that for a while and it sucked so I learned what I needed to learn to scrape this together.

Unfortunately, this does not take all manual labor out of the process as I am not skilled enough to make that leap. Important manual steps in this process are 1) Downloading the .odm files from overdrive, and 2) Adding them to wherever it is you want to access them whether it be a server, etc.

I will note that I am not an expert. I taught myself how to use python and bash in order to try and automate a process that I was getting frustrated by. With that being said I welcome anyone who has stumbled across this to take it and improve it for themselves. I also apologize to anyone using this who gets exasperated by any stupid mistakes or redundant processes I created along the way. If there were better solutions out there I would have used them instead of making this but as it stands now I couldn't find anything out there that automated the process to this extent so, for now, we all have to deal.

Note: This code assumes you have installed the following:

chbrown/overdrive
python3.10
pydub
ffmpeg
mutagen

You can reference https://github.com/chbrown/overdrive for setup on the chbrown script as well as tips and tricks for all things Overdrive.

I've organized my directory into the following folder structures mainly because I find it easier to follow the process when I'm visualizing the steps, but it should go without saying that you can mix and match this to your liking.

BOOKS
    00_ARCHIVE
    01_ANNEX
    02_CIRCULATION
    03_BOOKSHELF

The order of operations for the whole process is as follows:
1) Download ODM's
2) Run overdrive_full.sh
    i) Unpack odm's & add to annex along with metadata file
    ii) Extract list of chapters
    iii) Format metadata into xml
    iv) Convert chapter start times to ms
    v) Create final labels file showing chapter durations
    vi) Import mp3's end to end and export chapterized versions to circulation using labels file
    vii) Add metadata to the chapterized mp3's including track numbers and any simple metadata provided by Overdrive and move them to the bookshelf
3) Optional but Recommended: Use seanap's audible sources for mp3tag to correct and expand metadata for each book.
    I say optional because if your goal here is to just extract chapterized versions of the odm mp3's and start listening this isn't necessary. But for anyone like me who get's a bit picky about the way their library is formatted going the extra mile to addend all the proper metadata here is key. Another issue that arises with the original process is that Overdrive's metadata files are heavily lacking in details. As a result it's often the case that narrator names get messed up etc. If you care about precision this extra step is key.
4) Add to your server

You can find a lot of great advice and detailed walk-throughs on how to setup Plex libaries with audiobook functionality here: https://github.com/seanap/Plex-Audiobook-Guide

I decided not to involve an automated mb4 script in this because I've found that that process is still a bit manual for me. The reason being that I like packaging mb4's based around parts instead of tossing the full book inside of one or two. It's difficult to figure out a way of automating that given the lack of clear delineation of parts so I'm keep it manual for now.

And lastly all of this was inspired by my discovery of lcharlick's Prologue App (https://prologue.audio/), which, in my opinion, is the best iOS app for all things personal audiobooks collection. This whole process has been built around optimizing my experience using that app in tandem with Plex but it should be malleable to other systems with a little tweaking here and there.

Thanks to:
chbrown for creating and maintaining https://github.com/chbrown/overdrive
ex-nerd for the wonderful code "extract_overdrive_chapters.py"
seanap for the Plex Audiobook Guide
