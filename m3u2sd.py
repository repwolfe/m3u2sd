'''
Created on 2015-08-11

@author: robbie
'''
from __future__ import division
import io, os, sys, shutil, argparse, ntpath

FILE_ENCODING = "utf-8-sig"     # Unicode and removes any BOM information at the beginning of the playlist
SONG_EXTENSIONS = (".mp3", ".m4a")
EXTENSIONS_PREFIX = "#"
MUSIC_ROOT = "C:\Music\\"
SD_ROOT = "/<microSD1>/"

def update(args):
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
    with io.open(playlistPath, "r", encoding=FILE_ENCODING) as f:
        for numLines, line in enumerate(f):
            if line[0] == EXTENSIONS_PREFIX:      # don't count m3u extension information
                numExtensions = numExtensions + 1

    numLines = numLines - numExtensions + 1    # numLines starts at 0
    lineCount = 0
    with io.open(playlistPath, "r", encoding=FILE_ENCODING) as originalPlaylist, io.open(newPlaylistPath, "w", encoding=FILE_ENCODING) as newPlaylist:
        for line in originalPlaylist:
            line = line.rstrip("\r\n")
            if line[0] == EXTENSIONS_PREFIX:
                # m3u extension information, optionally write it to the new playlist
                if saveExtensions:
                    newPlaylist.write(line + "\n")
                else:
                    pass
            else:
                # Extract the folder the file is in (ignoring irrelevant parent folders))
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

def delete(args):
    playlistSongs = set()   # The union of all the playlist songs (assuming song file names are unique)
    sdcardSongs = set()     # All of the song files on the SD card
    filenamesToFullPath = {} 

    # Create the union of all of the songs in all of the playlists passed in
    for playlist in args.playlists:
        with io.open(playlist, "r", encoding=FILE_ENCODING) as playlist:
            for line in playlist:
                line = line.rstrip("\r\n")
                if line[0] != EXTENSIONS_PREFIX:
                    playlistSongs.add(ntpath.basename(line))   # Store the file name

    # Walk through the SD card folder structure and find all of the song files
    for root, dirs, files in os.walk(unicode(args.sdRoot, FILE_ENCODING)):
        for file in files:
            if file.lower().endswith(SONG_EXTENSIONS):
                sdcardSongs.add(file)
                # Store the full filename to later be able to delete the file
                filenamesToFullPath[file] = os.path.join(root, file)

    deletedFiles = sdcardSongs - playlistSongs

    if not deletedFiles:
        print "Nothing to delete"
    else:
        print "Files to be deleted:"
        for file in deletedFiles:
            print filenamesToFullPath[file]
        response = raw_input("Please confirm you'd like to delete these files [y/n}: ")
        if (response.lower().rstrip("\r\n") == "y"):
            for file in deletedFiles:
                os.remove(filenamesToFullPath[file])
        print "Done!"

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser()
    subParser = parser.add_subparsers()

    # The update command
    updateParser = subParser.add_parser("update", help="Takes an m3u playlist of songs and properly places them on an SD card.")
    updateParser.add_argument("playlistPath")
    updateParser.add_argument("finalRoot")
    updateParser.add_argument("--saveExtensions", action="store_true", help="Save the m3u extension information to the new playlist")
    updateParser.add_argument("--replaceAll", action="store_true", help="Replace existing mp3 files")
    updateParser.set_defaults(func=update)
    
    # The delete command
    deleteParser = subParser.add_parser("delete", help="Delete any music files on the SD card not in the given playlists")
    deleteParser.add_argument("sdRoot")
    deleteParser.add_argument("playlists", nargs="+", help="The playlists containing the songs to keep")
    deleteParser.set_defaults(func=delete)

    args = parser.parse_args()

    # Call the correct command function
    args.func(args)
