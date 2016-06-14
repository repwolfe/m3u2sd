# m3u2sd
Takes a playlist file and copies its songs to an SD card, and creates a new playlist with updated file locations

# Running instructions
 - First step is replace the MUSIC_ROOT variable with the folder that contains all of your songs
 - Replace the SD_ROOT variable with the name your MP3 device gives to the SD card root folder 

Run the script with the following parameters: TODO - UPDATE THIS
 - playlistPath the path to the playlist to copy to the SD card
 - finalRoot the final root location to store the music files on the SD card
 - (optional) saveExtensions save the m3u extension information to the new playlist (default False)
 - (optional) replaceAll boolean if should replace existing mp3 files (default False)