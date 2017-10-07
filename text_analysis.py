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

training_data = training_data[1:]
training_data = [x.split(",") for x in training_data]

gene = [x[1] for x in training_data]
variation = [x[2] for x in training_data]
category = [int(x[3][0]) for x in training_data]
category = np.array(category)
category_twops = 2 ** (category - 1)

# --------------
# Clean Synopsis Data
# --------------
synopses_text = [x.strip() for x in synopses_text]

full_dict = defaultdict(int)
for synopses_line in synopses_text:
    words = synopses_line.split()
    for word in words:
        full_dict[word] += 1

sorted_dictionary_tuplelist = sorted(full_dict.items(), key=operator.itemgetter(1), reverse=True)

sorted_dictionary_list = [itemtuple[0] for itemtuple in sorted_dictionary_tuplelist]
sorted_dictionary_index = {sorted_dictionary_list[i]: i for i in range(0, len(sorted_dictionary_list))}

# --------------
# Wordcount Matrix
# --------------
wordcount_doc = np.zeros(shape=(len(synopses_text), len(sorted_dictionary_list)), dtype=np.int16)
for synopses_line_no in range(0, len(synopses_text)):
    words = synopses_text[synopses_line_no].split()
    for word in words:
        wordcount_doc[synopses_line_no, (sorted_dictionary_index[word])] += 1


# --------------
# Existence Matrix
# --------------
wordexists_doc = np.zeros(shape=(len(synopses_text), len(sorted_dictionary_list)), dtype=np.int16)
np.copyto(wordexists_doc, wordcount_doc)
wordexists_doc[wordexists_doc != 0] = 1
# --------------
# Category-wise split
# --------------
exist_cat_list = []
count_cat_list = []
for i in range(1, 10):
    exist_cat_list.append(wordexists_doc[np.where(category == i)[0], :])
    count_cat_list.append(wordcount_doc[np.where(category == i)[0], :])

# --------------
# Row-wise sums
# --------------
numdocs_word = np.zeros(shape=(9, len(sorted_dictionary_list)), dtype=np.int16)
num_occurances_indoc_word = np.zeros(shape=(9, len(sorted_dictionary_list)), dtype=np.int32)
prob_occurances_indoc_word = np.zeros(shape=(9, len(sorted_dictionary_list)), dtype=np.float)
for i in range(0, 9):
    numdocs_word[i,] = np.sum(exist_cat_list[i], axis=0)
    num_occurances_indoc_word[i,] = np.sum(count_cat_list[i], axis=0)

# Get probabilities of word counts per page
prob_occurances_indoc_word = np.zeros(shape=(9, len(sorted_dictionary_list)), dtype=np.float)
prob_occurances_indoc_word = num_occurances_indoc_word/np.sum(num_occurances_indoc_word,axis=0)


# We are going to find out weights for each word. This weight is going to be based on two factors.

# Constants
alpha = 0.5
beta = 25
transform_power = 2.5
numwords = np.ma.count(prob_occurances_indoc_word,axis=1)[0]
mean = np.sum(prob_occurances_indoc_word,axis=1)/numwords
mean_tr = (mean*9)**transform_power

prob_occurances_indoc_word_tr = (prob_occurances_indoc_word*9)**transform_power
mean_shaped = np.reshape(np.repeat(mean_tr,numwords),(9,numwords))
part_a_wt = np.sum((prob_occurances_indoc_word_tr-mean_shaped)**2,axis=0)**alpha
part_b_wt = np.log(np.sum((num_occurances_indoc_word)**2,axis=0))/np.log(beta)
print(np.max(part_a_wt))
print(np.max(part_b_wt))
wts_arr = part_a_wt*part_b_wt
print("part_a_wt")
print(part_a_wt[1:10])
print(part_a_wt[160:165])
print("wts_array")
print(wts_arr[1:10])
print(wts_arr[160:165])

# IDHL indicates category 8 or 9
print("numdocs_word")
print(numdocs_word[:, 1:12])
print("num_occurances_indoc_word")
print(num_occurances_indoc_word[:, 1:12])
# np.save("cleaned/outputtrainmatrix", wordcount_doc )
