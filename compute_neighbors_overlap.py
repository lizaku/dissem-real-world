from composes.utils import io_utils
from composes.similarity.cos import CosSimilarity
import sys
import codecs
import json

''' Extracting neighbors from VG count-based space and BNC entropix space '''

obj_freq_file = 'vg_clusters_labels.txt'
obj_freq = {}

freq = codecs.open(obj_freq_file, 'r', 'utf-8')
for line in freq:
    word, label = line.lower().strip().split('\t')
    word = word.replace(' ', '_')
    obj_freq[word] = label

print(len(obj_freq))

#model = sys.argv[1]
#word = sys.argv[2]
        
def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / float(len(s1.union(s2)))

def single_model(word, model):

    PATH = '../dissect_spaces/mine/'
    #load two spaces
    my_space = io_utils.load(PATH + model)
    print(word)
    #composes_space = io_utils.load('EN-wform.w.2.ppmi.svd.500.txt')

    #print my_space.id2row
    #print my_space.cooccurrence_matrix
    #print composes_space.id2row
    #print composes_space.cooccurrence_matrix

    #get the top two neighbours of "car" in aripheral space 
    print my_space.get_neighbours(word, 10, CosSimilarity()) 
                              #space2 = composes_space)
                              
def two_models(obj_freq):
    PATH = 'models/'
    #load two spaces
    genome_space = io_utils.load(PATH + 'VG_relations_f10.pkl')
    #bnc_space = io_utils.load(PATH + 'bnc_sample.pkl')
    bnc = {}
    with open('bnc_entropix_neighbors.txt') as n:
        for line in n:
            main, neighbors = line.strip().split('\t')
            neighbors = neighbors.split()
            bnc[main] = neighbors
    overlap = codecs.open('overlap_bnc_15.csv', 'w', 'utf-8')
    overlap.write('Word\tCluster\tJaccard BNC-Genome\tGenome neighbors\tBNC_normalized neighbors\n')
    res_dic = {}
    for obj in obj_freq:
        label = obj_freq[obj]
        #print(obj)
        try:
            g_n = [x[0] for x in genome_space.get_neighbours(obj, 15, CosSimilarity())]
            b_n = bnc[obj]
            #b_n = [x[0] for x in bnc_space.get_neighbours(obj, 30, CosSimilarity())]
            j1 = jaccard_similarity(g_n, b_n)
            res_dic[obj] = [label, j1, g_n, b_n]
        except KeyError:
            print(obj, 'not_found')
            continue
    for key, value in sorted(res_dic.iteritems(), key=lambda (k,v): (v[1],k)):
        try:
            overlap.write('\t'.join([key.decode('utf-8'), str(value[0]).decode('utf-8'), str(value[1]).decode('utf-8'), ' '.join(value[2]), ' '.join(value[3])]) + '\n')
        except:
            continue
    overlap.close()
                              
two_models(obj_freq)
#single_model(word, model)
