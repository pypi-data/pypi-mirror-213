# Welcome to TT_WIZARD_CORE!

This projects provides an operating system independent backend to download and manage *.gme-files / audio files for the TipToi pen sold by Ravensburger. By removing the hassle to deal with file versioning and download servers, it especially enables the creation of tools for operating systems that are currently not officially supported by the manufacturer itself (like Linux). **TT_WIZARD_CORE** only uses the official servers (i.e. hosted by the manufacturer) to download any media files! 

## Following operations are currently supported:
- Searching the names of all currently published TipToi media for a keyword (e.g. "puzzle" to get all puzzles listed).
- Picking and downloading selected media from the search results above.
- Checking whether an already downloaded media file needs an update or not. (Attention: Files without recent updates may be flagged to require an update, even though no newer versions are available. This is a known issue.) 
- Auto update of media files that are already loaded to the TipToi pen

## Planned features
- Auto detect of pen mount point

## Installation of released version

Use pip to install:

```python
pip install tt_wizard_core
```
 
## Usage

```python
#!/usr/bin/env python

# if installed using pip
from tt_wizard_core import tt_wizard_core

# if not installed using pip and using source code
#from src.tt_wizard_core import tt_wizard_core

print("Welcome to an example of TT_WIZARD_CORE!")

# Create an tt_wizard_core object and provide it with the path to your pen,
# otherwise the current directory is used.
# A list of all available media files is downloaded automatically.
print("What is the path to your TipToi pen?")
penPath = str(input())
ttwiz = tt_wizard_core(penPath)
#if len(penPath) < 1:
#    penPath = ""
#    ttwiz = tt_wizard_core()

# Provide a string to search in the list of available media. 
print("Please enter keyword to search avaiable media for: ")
keyword = str(input())

# Search for string and receive a python list of media titles that partially match.
print("Found following media:")
searchResult = ttwiz.searchEntry(keyword)
num = 0
for item in searchResult:
    print(str(num) + ": " + item)
    num = num + 1

# Decide on which one to download and download media to folder specified in first step.
print("Which one do you like to download?")
chosenNum = int(input())
titleAsList = [searchResult[chosenNum]]
ttwiz.downloadMedia(titleAsList) #searchResult[chosenNum] is "<<fileName>>.gme"

# Do you want to download all available files?
#allMediaFilesList = ttwiz.getAllAvailableTitles()
#ttwiz.downloadMedia(allMediaFilesList)

# Pass the file name to retrieve information on whether an update is suggested or not.
#print("Update? " + str(ttwiz.checkForUpdate(searchResult[chosenNum], penPath))) # when >>penPath<< is different from the one configured in the constructor
print("Update? " + str(ttwiz.checkForUpdate(searchResult[chosenNum])))

# Perform automatic update on already downloaded media files.
print("Files updated: " + str(ttwiz.performAutoUpdate(dryRun=True)))
```

# Disclaimer and Trademark Notice

NOTE: This package is not verified by, affiliated with, or supported by Ravensburger® AG. TipToi® and Ravensburger® are registered trademarks or trademarks of Ravensburger® AG, in the Germany and/or other countries. These and all other trademarks referenced in this Software or Documentation are the property of their respective owners. The trademarkes are mentioned for reference only.