from __future__ import division
import numpy as np
from scipy import *
from scipy.sparse import *
import sqlite3
import sklearn
import io
from datetime import datetime
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import random

## Get two similarity matrices
#with open('Output/similarity_CF.p', 'rb') as f:
#    similarity_matrix = pickle.load(f)
#
#with open('Output/similarity_lyrics.p', 'rb') as f:
#    similarity_matrix2 = pickle.load(f)


# Get the two artist dicts
with open('Output/artists_dict_CF_red.p', 'rb') as f:
    artistsCF = pickle.load(f)

with open('Output/artists_dict_lyrics_red.p', 'rb') as f:
    artistsLyrics = pickle.load(f)

# Calculate similarity matrix WITHOUT TDIDF weighting
# Transform artists dict to a sparse matrix
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(artistsCF.values())
#print X_train_counts
#print X_train_counts.A

# Train the tf-idf model
from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
#print X_train_tf

# Compute cosine similarity matrix
from sklearn.metrics.pairwise import cosine_similarity
similarity_matrix = cosine_similarity(X_train_counts)

print "Finished with similarity matrix of CF"

## Save similarity matrix of CF
#with open('Output/similarity_CF.p', 'wb') as f:
#    pickle.dump(similarity_matrix, f)

# Determine k NN
kNN = 10
CFnearest_neighbors = []

for i in range(0,len(similarity_matrix)):
    sorted_similarity = np.argsort(similarity_matrix[i]).tolist()[::-1]
    CFnearest_neighbors.append(sorted_similarity[1:(kNN+1)])
    
print "Finished with nearest neighbors of CF"
    
# Calculate similarity matrix WITH TDIDF weighting
# Transform artists dict to a sparse matrix
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(artistsLyrics.values())
#print X_train_counts
#print X_train_counts.A

# Train the tf-idf model
from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
#print X_train_tf

# Compute cosine similarity matrix
from sklearn.metrics.pairwise import cosine_similarity
similarity_matrix2 = cosine_similarity(X_train_tf)

print "Finished with similarity matrix of Lyrics"

## Save similarity matrix of CF
#with open('Output/similarity_lyrics.p', 'wb') as f:
#    pickle.dump(similarity_matrix2, f)

# Determine k NN
kNN = 10
LYRnearest_neighbors = []

for i in range(0,len(similarity_matrix2)):
    sorted_similarity = np.argsort(similarity_matrix2[i]).tolist()[::-1]
    LYRnearest_neighbors.append(sorted_similarity[1:(kNN+1)])
    
print "Finished with nearest neighbors of Lyrics"

for i in range(0,50):
    intersectionTest = set(CFnearest_neighbors[i]).intersection(LYRnearest_neighbors[i])
    print len(intersectionTest)


### CALCULATE RANK BIASED OVERLAP
overlap = []
for i in range(0,len(CFnearest_neighbors)):
    intersection = []
    for j in range(1,len(CFnearest_neighbors[i])):
        intersection.append(len(set(CFnearest_neighbors[i][:(j)]).intersection(LYRnearest_neighbors[i][:(j)]))/(j))
    overlap.append(sum(intersection)/kNN)

# Calculate average overlap
print overlap[:100]
meanOverlap = sum(overlap)/len(overlap)
print meanOverlap

### CALCULATE RANK BIASED OVERLAP FOR RANDOM SET
overlap = []
for i in range(0,len(CFnearest_neighbors)):
    intersection = []
    sample = random.sample(xrange(1, len(CFnearest_neighbors)), 100)
    for j in range(1,len(CFnearest_neighbors[i])):
        intersection.append(len(set(CFnearest_neighbors[i][:(j)]).intersection(sample[:(j)]))/(j))
    overlap.append(sum(intersection)/kNN)

# Calculate average overlap
print overlap[:100]
meanOverlap = sum(overlap)/len(overlap)
print meanOverlap
    



