import numpy as np
from scipy import *
from scipy.sparse import *
import sqlite3
import sklearn
import io
from datetime import datetime
import networkx as nx
import pickle
    
# Open songs dict
with open('Output/songs_dict_lyrics.p', 'rb') as f:
    songs = pickle.load(f)

# Connect to lastfm DB
conn = sqlite3.connect('DBs/lastfm_tags.db')
c = conn.cursor()

# Connect to artist DB
conn2 = sqlite3.connect('DBs/track_metadata.db')
c2 = conn2.cursor()

# Iterate through each song in the songs dict, get the tags, get the artist,
#     and add the tags to an artist dict if they aren't already there
artistTags = {}

counter = 0

for i in songs.keys():
    #Get tags
    c.execute("SELECT tags.tag FROM tid_tag, tids, tags WHERE tags.ROWID=tid_tag.tag AND tid_tag.tid=tids.ROWID and tids.tid='%s'" %i)
    tags_query = c.fetchall()
    tags = tags_query
    
    counter += 1
    
    print str(counter) + " out of " + str(len(songs.keys()))
    
    #Get artist
    c2.execute("SELECT (artist_name) FROM songs WHERE track_id = '%s'" %i)
    artist_query = c2.fetchone()
    if artist_query is not None:
        artist = artist_query[0]
    else:
        print str(counter) + " not in set."
        continue
        
    #Add artist to songsTags if it's not in there
    if artist not in artistTags:
        artistTags[artist] = []
    
    #Add tags
    for j in tags:
        
        # Check if the tag is already accounted for
        if j not in artistTags[artist]:
            artistTags[artist].append(j)

conn.close()
conn2.close()

# How many artists
print "there are " + str(len(artistTags.keys())) + " artists."

# Open reduced artist set
with open('Output/artists_dict_lyrics_red.p', 'rb') as g:
    redArtists = pickle.load(g)

redArtistTags = {}

#Iterate through artistTags and see if they are in reduced set
for i in artistTags:
    if i in redArtists:
        redArtistTags[i] = artistTags[i]

# How many reduced?
print "there are " + str(len(redArtistTags.keys())) + " reduced artists."

# Print a few
for i in range(0,5):
    print redArtistTags[redArtistTags.keys()[i]]

# Save artistTags
with open('Output/artist_tags_red.p', 'wb') as h:
    pickle.dump(redArtistTags, h)


    
    

