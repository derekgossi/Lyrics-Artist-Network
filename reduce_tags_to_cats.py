import numpy as np
from scipy import *
from scipy.sparse import *
import sqlite3
import sklearn
import io
from datetime import datetime
import networkx as nx
import pickle

# Open tags
with open('Output/artist_tags_red2.p', 'rb') as f:
    artistTags = pickle.load(f)

# Tag category dict
tagCats = {}

tagCats["rock"] = ["rock","classic rock", "hard rock", "Progressive rock", "pop rock", "soft rock", "rock n roll", "Rock and Roll"]
tagCats["pop"] = ["pop", "pop rock"]
tagCats["alternative"] = ["alternative", "alternative rock", "indie alternative"]
tagCats["indie"] = ["indie", "indie rock", "indie pop"]
tagCats["electronic"] = ["electronic", "electronica", "electro", "House", "trance", "techno", "progressive trance", "deep house"]
tagCats["female"] = ["female vocalists", "female vocalist", "female", "female vocals", "female vocal"]
tagCats["dance"] = ["dance", "party", "club"]
tagCats["jazz"] = ["jazz", "jazzy"]
tagCats["folk"] = ["singer-singwriter", "folk","acoustic","folk rock","singer songwriter"]
tagCats["metal"] = ["metal", "heavy metal", "death metal", "Progressive metal", "black metal", "Power metal", "Gothic metal", "melodic metal", "doom metal", "thrash metal", "metalcore", "Nu Metal"]
tagCats["relaxing"] = ["chillout", "Mellow", "chill", "relax", "relaxing", "calm", "chill out"]
tagCats["soul"] = ["soul", "rnb", "funk", "r&b", "RB", "r and b"]
tagCats["male"] = ["male vocalists", "male vocalist", "male vocals", "male"]
tagCats["hiphop"] = ["Hip-Hop", "hip hop", "rap", "hiphop"]
tagCats["punk"] = ["punk", "punk rock"]
tagCats["blues"] = ["blues", "blues rock"]
tagCats["country"] = ["country", "classic country"]
tagCats["positive"] = ["fun", "happy", "upbeat", "Energetic", "Uplifting", "feel good", "energy", "positive"]
tagCats["negative"] = ["sad", "melancholy", "melancholic", "dark", "moody", "Bittersweet"]
tagCats["reggae"] = ["reggae"]
tagCats["romantic"] = ["romantic", "love songs", "love song", "sensual", "sex", "sexy"]
tagCats["latin"] = ["latin", "spanish","latino"]
tagCats["christian"] = ["christian", "worship"]

# New tag dict
newTagDictByArtist = {}
newTagDictByTag = {}

for i in artistTags:
    newTagDictByArtist[i] = []
    for j in range(0,len(artistTags[i])):
        for k in tagCats:
            for l in range(0,len(tagCats[k])):
                if artistTags[i][j] == tagCats[k][l]:
                    #Check if this tag category is already added to the artist
                    if k not in newTagDictByArtist[i]:
                        newTagDictByArtist[i].append(k)

for i in tagCats:
    newTagDictByTag[i] = []
    for j in newTagDictByArtist:
        if i in newTagDictByArtist[j]:
            newTagDictByTag[i].append(j)

print newTagDictByTag["reggae"]
print newTagDictByTag["indie"]

# Save dicts
with open('Output/tags_by_artist.p', 'wb') as f:
    pickle.dump(newTagDictByArtist, f)

with open('Output/tags_by_tag.p', 'wb') as f:
    pickle.dump(newTagDictByTag, f)




   

