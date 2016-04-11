'''
Created on 2015-08-11

@author: robbie
'''
from __future__ import division
import io, os, sys, shutil, argparse

EXTENSIONS_PREFIX = "#"
MUSIC_ROOT = "C:\\Music\\"
SD_ROOT = "/<microSD1>/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Takes an m3u playlist of songs and properly places them on an SD card.")
    parser.add_argument("playlistPath")
    parser.add_argument("finalRoot")
    parser.add_argument("--saveExtensions", action="store_true", help="Save the m3u extension information to the new playlist")
    parser.add_argument("--replaceAll", action="store_true", help="Replace existing mp3 files")
    parser.add_argument("--deleteRemoved", action="store_true", help="Delete any music files on the SD card not on the playlist")

    args = parser.parse_args()
    playlistPath = args.playlistPath
    finalRoot = args.finalRoot
    saveExtensions = args.saveExtensions
    replaceAll = args.replaceAll
    deleteRemoved = args.deleteRemoved

    playlistName = os.path.basename(playlistPath)
    print "Opening playlist: %s" % playlistName

    newPlaylistPath = os.path.join(finalRoot, playlistName)
    finalRootWithoutDrive = os.path.splitdrive(finalRoot)[1].lstrip(os.sep)     # Remove the drive name and slashes

    # Get the number of lines in the playlist for a progress bar
    numLines = 0
    numExtensions = 0
    with open(playlistPath, "r") as f:
        for numLines, line in enumerate(f):
            if line[0] == EXTENSIONS_PREFIX:      # don't count m3u extension information
                numExtensions = numExtensions + 1

    numLines = numLines - numExtensions + 1    # numLines starts at 0
    lineCount = 0
    with io.open(playlistPath, "r", encoding="utf-8-sig") as originalPlaylist, io.open(newPlaylistPath, "w", encoding="utf-8-sig") as newPlaylist:
        for line in originalPlaylist:
            line = line.rstrip("\r\n")
            if line[0] == EXTENSIONS_PREFIX:
                # m3u extension information, optionally write it to the new playlist
                if saveExtensions:
                    newPlaylist.write(line + "\n")
                else:
                    pass
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
                        print songLocation
                        os.makedirs(dirName)
                    shutil.copyfile(line, finalLocation)

                # Print progress
                lineCount = lineCount + 1
                print "{0}% done ({1}/{2})".format((lineCount / numLines * 100), lineCount, numLines)