import numpy as np
from scipy import *
from scipy.sparse import *
import sqlite3
import sklearn
import io
from datetime import datetime
import networkx as nx
import pickle
    
# Open dict
with open('Output/artists_dict_CF_red.p', 'rb') as f:
    artists = pickle.load(f)
    
# Calculate similarity matrix WITHOUT TDIDF weighting
# Transform artists dict to a sparse matrix
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(artists.values())
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

print "Finished with similarity matrix"

# Determine k NN
kNN = 10
nearest_neighbors = []

for i in range(0,len(similarity_matrix)):
    sorted_similarity = np.argsort(similarity_matrix[i]).tolist()[::-1]
    nearest_neighbors.append(sorted_similarity[1:(kNN+1)])
    
print "Finished with nearest neighbors"

# Create edge matrix 
NNedges = []

for i in range(0,len(nearest_neighbors)):
    
    # Set of edges for one row
    edgeRow = [0]*len(nearest_neighbors)
    
    for j in range(0,kNN):
        edgeRow[nearest_neighbors[i][j]] = 1
    
    NNedges.append(edgeRow)

print "Finished with edge matrix"

# NX Graph
G=nx.DiGraph()

# Add nodes which are keys in the artists dict
G.add_nodes_from(artists.keys())

# Add edges
for i in range(0,len(NNedges)):
    for j in range(0, len(NNedges)):
        if(NNedges[i][j]>0 and i!=j):
            G.add_edge(artists.keys()[i],artists.keys()[j])

# Save G
with open('Output/CF_network.p', 'wb') as f:
    pickle.dump(G, f)
