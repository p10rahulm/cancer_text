
from collections import defaultdict
import operator
import numpy as np
import csv




with open("cleaned/training_synopses.txt", "r") as f:
    synopses_text = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
synopses_text = [x.strip() for x in synopses_text]

full_dict = defaultdict(int)
for synopses_line in synopses_text:
    words = synopses_line.split()
    for word in words:
        full_dict[word]+=1

sorted_dictionary_tuplelist = sorted(full_dict.items(), key=operator.itemgetter(1),  reverse=True)

sorted_dictionary_list = [itemtuple[0] for itemtuple in sorted_dictionary_tuplelist]
sorted_dictionary_index = {sorted_dictionary_list[i]:i for i in range(0,len(sorted_dictionary_list))}


outputmatrix = np.zeros(shape=(len(synopses_text),len(sorted_dictionary_list)), dtype=np.int8)

for synopses_line_no in range(0,len(synopses_text)):
    words = synopses_text[synopses_line_no].split()
    for word in words:
        outputmatrix[synopses_line_no,(sorted_dictionary_index[word]-1)] += 1

print(outputmatrix [0:20,])
np.save("cleaned/outputtrainmatrix", outputmatrix )

