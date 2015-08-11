'''
Created on 2015-08-11

@author: robbie
'''
from __future__ import division
import os, sys, shutil

MUSIC_ROOT = "C:\\Music\\"
SD_ROOT = "/<microSD1>/"

'''
@params playlistPath the path to the playlist to copy to the SD card
		finalRoot the final root location to store the music files
        replaceAll boolean if should replace existing mp3 files (optional)
'''
if __name__ == "__main__":
    if len(sys.argv) == 3:
        playlistPath, finalRoot = sys.argv[1:]
        replaceAll = False
    elif len(sys.argv) == 4:
        playlistPath, finalRoot, replaceAll = sys.argv[1:]

    if playlistPath == "" or finalRoot == "":
        raise Exception("Empty playlistPath or finalRoot")

    playlistName = os.path.basename(playlistPath)
    print "Opening playlist: %s" % playlistName

    newPlaylistPath = os.path.join(finalRoot, playlistName)
    finalRootWithoutDrive = os.path.splitdrive(finalRoot)[1].lstrip(os.sep)     # Remove the drive name and slashes

    # Get the number of lines in the playlist for a progress bar
    numLines = 0
    with open(playlistPath, "r") as f:
        for numLines, line in enumerate(f):
            pass

    lineCount = 0
    with open(playlistPath, "r") as originalPlaylist, open(newPlaylistPath, "w") as newPlaylist:
        for line in originalPlaylist:
            line = line.rstrip("\r\n")
            if line[0] == "#":
                # m3u extension information, simply write it to the new playlist
                newPlaylist.write(line + "\n")
            else:
                # Extract the folder the file is in (ignoring irrelevant parent folders)
                songLocation = os.path.relpath(line, MUSIC_ROOT)

                # Write to the new playlist file
                finalLocation = os.path.join(SD_ROOT, finalRootWithoutDrive, songLocation).replace("\\", "/")
                newPlaylist.write(finalLocation + "\n")

                # Copy the file to its new location (if it doesn't exist)
                finalLocation = os.path.join(finalRoot, songLocation)
                if replaceAll or not os.path.isfile(finalLocation):
                    # Make the directory if it doesn't exist
                    dirName = os.path.dirname(finalLocation)
                    if not os.path.exists(dirName):
                        os.makedirs(dirName)
                    shutil.copyfile(line, finalLocation)

            # Print progress
            lineCount = lineCount + 1
            print "{0}% done ({1}/{2})".format((lineCount / numLines * 100), lineCount, numLines)