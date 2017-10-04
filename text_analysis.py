# --------------
# Importing Libraries
# --------------

from collections import defaultdict
import operator
import numpy as np
import csv

# --------------
# Open Raw Data
# --------------
with open("cleaned/training_synopses.txt", "r") as f:
    synopses_text = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

with open("rawdata/training_variants.csv", "r") as f:
    training_data = f.readlines()

# --------------
# Clean meta data
# --------------

training_data = training_data [1:]
training_data = [x.split(",") for x in training_data]

gene = [x[1] for x in training_data]
variation = [x[2] for x in training_data]
category = [int(x[3][0]) for x in training_data]
category = np.array(category)
# print(category)
# print(len(category))
# --------------
# Clean Synopsis Data
# --------------
synopses_text = [x.strip() for x in synopses_text]

full_dict = defaultdict(int)
for synopses_line in synopses_text:
    words = synopses_line.split()
    for word in words:
        full_dict[word]+=1

sorted_dictionary_tuplelist = sorted(full_dict.items(), key=operator.itemgetter(1),  reverse=True)

sorted_dictionary_list = [itemtuple[0] for itemtuple in sorted_dictionary_tuplelist]
sorted_dictionary_index = {sorted_dictionary_list[i]:i for i in range(0,len(sorted_dictionary_list))}
print(len(sorted_dictionary_list))

# --------------
# Wordcount Matrix
# --------------
wordcount_doc = np.zeros(shape=(len(synopses_text),len(sorted_dictionary_list)), dtype=np.int8)

for synopses_line_no in range(0,len(synopses_text)):
    words = synopses_text[synopses_line_no].split()
    for word in words:
        wordcount_doc[synopses_line_no,(sorted_dictionary_index[word]-1)] += 1
print("wordcount")
print(wordcount_doc[0:20, ])

# --------------
# Existence Matrix
# --------------
wordexists_doc  = wordcount_doc
wordexists_doc[wordexists_doc  !=0] = 1
print("wordexists")
print(wordexists_doc [0:20, ])



# np.save("cleaned/outputtrainmatrix", wordcount_doc )

