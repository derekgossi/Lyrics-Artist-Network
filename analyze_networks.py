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


# Get the network
with open('Output/lyrics_network.p', 'rb') as f:
    G = pickle.load(f)
    
## Get the network
#with open('Output/CF_network.p', 'rb') as f:
#    G = pickle.load(f)
    
# Get tags by artist
with open('Output/tags_by_artist.p', 'rb') as f:
    tagsByArtist = pickle.load(f)

# Get artists by tags
with open('Output/tags_by_tag.p', 'rb') as f:
    tagsByTag = pickle.load(f)
    
### UNDIRECTED GRAPH
U = G.to_undirected()

### STATS
#print nx.diameter(U)*1.00
#print(nx.average_shortest_path_length(G))
#print(nx.average_shortest_path_length(U))
#print nx.average_clustering(U)

### SUBGRAPHS
## Create subgraphs
#subgraphs = {}
#for i in tagsByTag:
#    # i is a tag category and tagsByTag[i] is a list of artists
#    # we want the subgraph with only these artists
#    subgraph = G.subgraph(tagsByTag[i])
#    
#    # Subgraph dict has the tag category name as key and graph as value
#    subgraphs[i] = subgraph
#
#for i in subgraphs:
#    print i
#    numNodes = len(subgraphs[i].nodes())*1.0
#    numEdges = len(subgraphs[i].edges())*1.0
#    expectedRandomEdges = (numNodes*10)*(numNodes/len(G.nodes()))
#    edgesPerNode = numEdges/numNodes
#    print "Nodes: %.2f" % numNodes
#    print "Edges per node: %.2f" % edgesPerNode
#    print "Expected random edges: %.2f" % expectedRandomEdges
#    print "Actual edges %.2f" % numEdges
#    percentAboveRandom = numEdges/expectedRandomEdges
#    print "Actual to random %.2f" % percentAboveRandom
#    #print "Total possible edges: " + str(len(subgraphs[i].nodes())*10)
#    #print "Actual edges: " + str(len(subgraphs[i].edges()))
#    #clustering = len(subgraphs[i].edges())/(len(subgraphs[i].nodes())*10)
#    #print "Clustering: %.2f" % clustering
#    #print "CC: %.2f" % nx.average_clustering(subgraphs[i])
#    #perNodes = len(subgraphs[i].nodes())/len(U.nodes())
#    #perEdges = len(subgraphs[i].edges())/len(U.edges())
#    #print "Percent of edges to nodes: %.2f" % (perEdges/perNodes)


### DEGREE DISTRIBUTION
#degree_sequence=sorted(G.in_degree().values(),reverse=True) # degree sequence
##print "Degree sequence", degree_sequence
#dmax=max(degree_sequence)
#plt.loglog(degree_sequence,'b-',marker='o')
#plt.title("Collaborative Filtering Network - Indegree Distribution")
#plt.ylabel("degree")
#plt.xlabel("rank")
#plt.show()

### HIGHEST DEGREE NODES
#sortedIndegree = sorted(G.in_degree(),key=G.in_degree().get)
#sum = 0
#for i in sortedIndegree:
#    #Get tags for i
#    tags = tagsByArtist[i]
#    
#    print unicode(i) + ", " + unicode(G.in_degree(i)) + ", " + unicode(tags)
#
#print len(tagsByTag["indie"])
