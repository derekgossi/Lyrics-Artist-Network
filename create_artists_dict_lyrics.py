import numpy as np
from scipy import *
from scipy.sparse import *
import sqlite3
import sklearn
import io
from datetime import datetime
import networkx as nx
import pickle

# Connect to lyrics DB and get cursor
conn = sqlite3.connect('DBs/mxm_dataset.db')
c = conn.cursor()

# Initialize lyrics dict
lyrics = {}

# Counter
counter = 0

# Get lyrics by song id
for row in c.execute('SELECT * FROM lyrics'):

    # Song ID
    song_id = row[0]
    
    # Word in lyrics
    word = row[2]
    
    counter += 1
    if(counter % 100000 == 0):
        print counter
    
    # Number of times a word appears in a song
    num_words = row[3]
    
    # Check if song id is already in lyrics dict
    if song_id not in lyrics:
        lyrics[song_id] = ""
    
    # Add the word to the song's lyric string the number of times it appears
    for i in range(0,num_words):
        lyrics[song_id] += " "
        lyrics[song_id] += word

# Close connection
conn.close()

# Lyrics songs dict save
with open('Output/songs_dict_lyrics.p', 'wb') as f:
    pickle.dump(lyrics, f)


# Connect to metadata DB and get cursor
conn = sqlite3.connect('DBs/track_metadata.db')
c = conn.cursor()

# Initialize artists list
artists = []

# Artists dict
artistsDict = {}

# Iterate through song id dict and get artist to make artist dict
counter = 0
for i in lyrics.keys():
    c.execute("SELECT (artist_name) FROM songs WHERE track_id = '%s'" %i)
    artist_query = c.fetchone()
    artist = artist_query[0]
    
    counter += 1
    if(counter % 10000 == 0):
        print str(len(artistsDict.keys())) + " unique artists out of " + str(len(lyrics.keys())) + " songs " + str(counter)
    
    # Add artist to match index of lyrics array
    artists.append(artist)
    
    # Check if artist is in artist dict
    if artist not in artistsDict:
        artistsDict[artist] = ""
    
    # Add lyrics to that artist's lyrics in dict
    artistsDict[artist] += lyrics[i]
    artistsDict[artist] += " "

# Close connection
conn.close()

# Artists dict save
with open('Output/artists_dict_lyrics.p', 'wb') as f:
    pickle.dump(artistsDict, f)
