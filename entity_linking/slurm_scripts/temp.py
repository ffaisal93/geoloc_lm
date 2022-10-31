import os
out_root  = '/scratch/ffaisal/ner_linking'

for x in os.listdir(out_root):
    discarded = ['.DS_Store']
    print( x)
