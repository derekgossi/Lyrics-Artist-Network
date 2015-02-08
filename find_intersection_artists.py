import numpy as np
from scipy import *
from scipy.sparse import *
import sqlite3
import sklearn
import io
from datetime import datetime
import networkx as nx
import pickle

# Get artists lyrics dict
with open('Output/artists_dict_lyrics.p', 'rb') as f:
    artistsLyrics = pickle.load(f)
    
# Get artists cf dict
with open('Output/artists_dict_CF.p', 'rb') as g:
    artistsCF = pickle.load(g)

# List of similar artists
intersectArtists = []

#Reduced dicts
artistsLyricsRed = {}
artistsCFRed = {}

for i in artistsLyrics.keys():
    #Check if it is in CF dict
    if i in artistsCF.keys():
        #Add to intersection list
        intersectArtists.append(i)
        
        #Add to reduced dicts
        artistsLyricsRed[i] = artistsLyrics[i]
        artistsCFRed[i] = artistsCF[i]

#Save reduced dicts
with open('Output/artists_dict_CF_red.p', 'wb') as h:
    pickle.dump(artistsCFRed, h)

with open('Output/artists_dict_lyrics_red.p', 'wb') as i:
    pickle.dump(artistsLyricsRed, i)
        


