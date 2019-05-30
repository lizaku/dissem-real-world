import numpy as np
import scipy.sparse
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
import heapq

''' Extracting neighbors from entropix models '''

indices = {}
indices_inv = {}
non_overlap = set()
all_words = {}
print('loading data...')
with open('clustered_words.txt') as b:
    for line in b:
        non_overlap.add(line.strip())
with open('models/bnc_rawtext.mincount-10.win-2.vocab') as v:
    for line in v:
        col, word = line.strip().split('\t')
        all_words[col] = word
        if word in non_overlap:
            indices[word] = col
            indices_inv[col] = word
            
matrix = scipy.sparse.load_npz('models/bnc_rawtext.mincount-10.win-2.ppmi.npz')
word_matrix = None
inds = []
print('computing similarities...')
for word in indices:
    #print(word, indices[word])
    inds.append(indices[word])
    row = matrix.getrow(indices[word]).toarray()
    if word_matrix is None:
        word_matrix = row
    else:
        word_matrix = np.vstack((word_matrix, row))

dist_out = 1-pairwise_distances(word_matrix, metric="cosine")
i = 0
with open('bnc_ppmi_entropix_neighbors.txt', 'w', encoding='utf-8') as n:
    for row in dist_out:
        neighbors = heapq.nlargest(15, range(len(row)), row.take)
        n.write(indices_inv[str(inds[i])] + '\t' + ' '.join([all_words[str(x)].lower() for x in neighbors]) + '\n')
        #print(indices_inv[str(inds[i])], 'neighbors', [all_words[str(x)] for x in neighbors])
        i += 1
