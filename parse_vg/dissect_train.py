from composes.semantic_space.space import Space
from composes.utils import io_utils
from composes.transformation.scaling.ppmi_weighting import PpmiWeighting
from composes.transformation.scaling.normalization import Normalization

PATH = 'dissect_spaces/mine/'
#ppmi weighting

print('Checking for errors...')
with open(PATH + 'corpus_small.sm') as f:
    with open(PATH + 'ukwac_correct.sm', 'w') as n:
        for line in f:
            values = line.split()
            if len(values) == 3:
                n.write(line)
            else:
                continue
            
print('Building the space...')
#create a space from co-occurrence counts in sparse format
my_space = Space.build(data = PATH + "ukwac_correct.sm",
                       rows = PATH + "corpus_small.rows",
                       cols = PATH + "corpus_small.rows",
                       format = "sm")
                       
my_space = my_space.apply(PpmiWeighting())
my_space = my_space.apply(Normalization())

#export the space in sparse format
#my_space.export(PATH + "result_attributes_f10", format = "sm")
    
#export the space in dense format
#my_space.export(PATH + "result_relations_f10", format = "dm")
io_utils.save(my_space, PATH + 'ukwac_norm_ppmi_without_pos.pkl')
