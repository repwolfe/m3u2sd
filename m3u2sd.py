'''
Created on 2015-08-11

@author: robbie
'''

import os, sys

'''
@params startingPlaylist the path to the playlist to copy to the SD card
		finalRoot the final root location to store the music files
'''
if __name__ == "__main__":
    startingPlaylist, finalRoot = sys.argv[1:]

    if startingPlaylist == "" or finalRoot == "":
        raise Exception("Empty startingPlaylist or finalRoot")

    with open(startingPlaylist, "rb") as originalPlaylist:
        for line in originalPlaylist:
            print line