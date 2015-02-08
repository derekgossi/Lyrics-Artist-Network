import numpy as np
from scipy import *
from scipy.sparse import *
import sqlite3
import sklearn
import io
from datetime import datetime
import networkx as nx
import pickle
import csv

# Start timer
startTime = datetime.now()

# Counter
counter = 0

# Open file with user play count data
with open('DBs/train_triplets.txt') as f:
    reader = csv.reader(f, delimiter="\t")
    
    songs = {}

    incrementer = 0
    
    for row in reader:
        # Song
        song = row[1]
        
        # See if song is already in dict
        if song not in songs:
            songs[song] = ""
        
        # How many times do we need to add the user entry to the dict?
        playCount = int(row[2])
        
        # Now that song is in dict, add the user to the entry the play count # of times
        for i in range(0,playCount):
            songs[song] += row[0]
            songs[song] += " "
        
        # Print iteration
        counter += 1
        if(counter % 100000 == 0):
            print counter
        
        # Incrementer
        incrementer += 1 
        
        if(incrementer >= 10000000):
            break

# Connect to metadata DB and get cursor
conn = sqlite3.connect('DBs/track_metadata.db')
c = conn.cursor()

# Initialize artists list
artists = []

# Artists dict
artistsDict = {}

# How many songs?
print len(songs.keys())

# Iterate through song id dict and get artist to make artist dict
for i in songs.keys():
    c.execute("SELECT (artist_name) FROM songs WHERE song_id = '%s'" %i)
    artist_query = c.fetchone()
    print artist_query
    print songs.keys().index(i)
    print " out of "
    print len(songs.keys())
    artist = artist_query[0]
    
    # Add artist to match index of lyrics array
    artists.append(artist)
    
    # Check if artist is in artist dict
    if artist not in artistsDict:
        artistsDict[artist] = ""
    
    # Add lyrics to that artist's lyrics in dict
    artistsDict[artist] += songs[i]
    artistsDict[artist] += " "

# Close connection
conn.close()

# Save artist query
with open('Output/artists_dict_CF.p', 'wb') as f:
    pickle.dump(artistsDict, f)

# Print time
print(datetime.now()-startTime)