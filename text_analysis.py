# ###############################
# Describing the algorithm for predicting the probabilities of each document being of a particular category below
# Each word is a probability vector which has 9 dimensions (as there are 9 categories)
# Probability of a document is the sum of the weighted probabilities of each word in the document.
# In other words we have set(words|document) and (category|document).
# From this, we can generate a table to have P(category), P(category|word) and P(word) in the training set
# ###############################
#
# Now we are given a test set of documents which has set(words|document). We need to find category of the document.
# More to the point, we need to find out category given an array of words
# Or in other words, we have to find P(category|set(words))
# P(category|sigma(Wi)) = sigma(P(category|Wi)*Alpha_i)) where alpha is the weight for each word
# Now how to find out the weight for each word.
#
# Before getting into what factors go into alpha, let us take up certain test cases
# Firstly,
# From this, we get certain rules:
# 1)  Probabilities closer to 1 are more important that weights closer to 0
# 2)  A random distribution has low information content,
#       for example, a distribution of (0.5, 0.5) in case of 2 categories
# 3)  There exists apriori a certain probability of categories.
#       For example category 1 occurring 8 times for category 2 occurring 1 time
# 4)  This apriori probability can be called the mean probability of categories
# 5)  Most words are likely to be to be distributed similar to the mean distribution of categories
# 6)  Common english words for example may have a distribution amongst categories similar to the mean probabilities.
# 7)  We are adding the probability distribution of each word to get the probability distribution of document.
# 8)  Therefore those close to mean should be given low weight as there are likely to be a large number of them
# 9)  Therefore distance from mean should be a factor in word weighting
#
#     We can choose to plot the probability vector on an n-dimensional surface (where n is the number of categories)
#     for ease of vector operations
#     Let us assume the mean is plotted at Mi and the words are Xi. We get some more rules:
#
# 10) In a two category case, the distance from mean can directly be used as a proxy for weight
# 11) In cases of higher than two categories, some axes can be less likely than others.
# 12) Therefore a word that has a high weight for those axes should be given an increased weight
# 13) Else it is likely to be drowned out by the large number of words which are similar to the Mean distribution
# 14) Distance from mean is constant across a circle in the plane of possible points (since sum (Xi) = 1)
# 15) But distance across less likely axis should be given more weight as compared to other axes as they occur less
#       For example, if Mi = (0.49,0.49,0.01), X1 = (0,0.99,0.01), X2 = (0.99,0,0.01) and X3 = (0,0,1)
#       Then, document containing set(X1,X2,X3) should be most likely category 3.
#       If weight was simply distance from mean, then D1 ~ 0.5, D2 ~ 0.5, D3 ~ 1.5 and
#       net probabilities ~(0.5,0.5,1.5) or (0.25,0.25,0.5)
# 16) This brings us to the need for transforming the space before applying the distance function.
# 17) *One transformation that could be chosen is to multiply each vector axis by 1/(Mi) before distance is calculated*
#
#     Coming back to information content in a vector, as noted in point (2),
# 18) We need to give higher weight to points which are higher than the expected value from random distribution
# 19) For an n category space, the expected value is Xi = 1/n
# 20) One categorization could be from plane to hyperbolic. But this gives issues of infinity at probability 1
# 21) To constrain the space, we could use an exponential function, but this works only for values greater than 1
# 22) An appropriate solution is to use a exponential transformation after multiplying by n, where n is num. dimensions
# 23) We can therefore use the transformation (Xi*n)^(lambda), where lambda is a tuning parameter
# 24) Further to take into account point (17) we can do a element-wise multiplication with 1/(Mi)
#       This is done to account for probability difference between the axes
# 25) The transformed space therefore is given by (Xi*n)^(lambda)*(1/Mi)
# 26) Lets call the mean in transformed space as Mi_tr and each of the word vectors as Xi_tr
# 27) Then the weight assigned can be distance(Mi_tr - Xi_tr)
#
#     This leaves us with another issue.
# 28) What about two words that lie at the same point on the vector space but are occuring a different number of times?
#       For example, X1 = (0.9,0.1), X2 = (0.9,0.1) but W1 = (9,1), W2 = (900,100). Which one has more information?
# 29) Due to law of large numbers, W2 has a higher likelihood of being the more accurate description of the probability
#       distribution than W1, which might be a random occurrence.
# 30) To include this as part of our weights, we use log(total word occurrences) as part of the weight for the word
#       Note to self: Could it be due to information entropy

# To summarize,
# 1) The probability distribution of a document = sigma(alpha*Xi)
#       where
#       alpha is word weight
#       Xi is P(Ci|word)
# 2) alpha is composed of two parts: (a) distance from mean in transformed space and (b) log of total occurrences
# 3) Transformed space is defined as ((Xi*n)^lambda)*(1/Mi). We can assume lambda to be 2 for starters
# 4) Mi_tr = ((Mi*n)^lambda)*(1/Mi); Xi_tr = ((Xi*n)^lambda)*(1/Mi)
# 5) We can assume euclidean distance. alpha  proportional to distance(Mi_tr - Xi_tr)
# 6) alpha also proportional to log(sigma(Wi)) where Wi is word count of W in category i
# 7) We can scale each of the above by tuning parameters beta and gamma (assumed to be 2 and 1 for now)
#       Note to self: There is likely another dependence on document length, which we have not accounted for.
# 8) therefore alpha = distance(Mi_tr - Xi_tr)^beta * log(sigma(Wi))^gamma
#
# ###############################



# --------------
# Importing Libraries
# --------------

import operator
from collections import defaultdict

import numpy as np

# --------------
# Open Raw Data
# --------------
with open("cleaned/training_synopses.txt", "r") as f:
    synopses_text = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line

with open("rawdata/training_variants.csv", "r") as f:
    training_data = f.readlines()

# Test Data
with open("cleaned/stage2_test_synopses.txt", "r") as f:
    test_synopses_text = f.readlines()


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
prob_occurances_indoc_word = num_occurances_indoc_word / np.sum(num_occurances_indoc_word, axis=0)

# -------------
# Constants
# -------------
# Please check the part_A_power and part_B_power weights should depend on document length
PART_A_POWER = 2
PART_B_POWER = 2
WORDS_LOG = 30
LAMBDA = 2
NUM_DIM = len(prob_occurances_indoc_word)
NUMWORDS = np.ma.count(prob_occurances_indoc_word, axis=1)[0]

# -------------
# Calculating Mean and transformed mean
# -------------
mean = np.sum(prob_occurances_indoc_word, axis=1) / NUMWORDS
mean_tr = (1 / mean) * ((mean * NUM_DIM) ** LAMBDA)

prob_occurances_indoc_word_tr = (prob_occurances_indoc_word * NUM_DIM) ** LAMBDA
mean_inv_shaped = np.reshape(np.repeat(1/mean, NUMWORDS), (NUM_DIM, NUMWORDS))
prob_occurances_indoc_word_tr = prob_occurances_indoc_word_tr*mean_inv_shaped
mean_tr_shaped = np.reshape(np.repeat(mean_tr, NUMWORDS), (NUM_DIM, NUMWORDS))
part_a_wt = np.sum((prob_occurances_indoc_word_tr - mean_tr_shaped ) ** 2, axis=0)**0.5
part_b_wt = (np.log(np.sum(num_occurances_indoc_word ** 2, axis=0)**0.5) / np.log(WORDS_LOG))
word_wts =(part_a_wt**PART_A_POWER)*(part_b_wt **PART_B_POWER)
avg_word_wt = np.average(word_wts)
word_wts = word_wts/avg_word_wt

################################
## Checks: This section for some checks on model
#
# print("np.max(np.sum(wordcount_doc,axis=1))")
# print(np.max(np.sum(wordcount_doc,axis=1)))
# print("np.average(np.sum(wordcount_doc,axis=1))")
# print(np.average(np.sum(wordcount_doc,axis=1)))
#
# print("max part_a_wt")
# print(np.max(part_a_wt))
# print("max part_b_wt")
# print(np.max(part_b_wt))
# print("max word_wts")
# print(np.max(word_wts))
# IDHL indicates category 8 or 9. This is word 163 and should have a high weight
# print("part_a_wt[1:10]")
# print(part_a_wt[1:10])
# print("part_a_wt[160:165]")
# print(part_a_wt[160:165])
# print("word_wts[0:9]")
# print(word_wts[0:9])
# print("word_wts[160:165]")
# print(word_wts[160:165])
################################

#--------
# Work with Test data
#--------
test_synopses_text = [x.strip() for x in test_synopses_text]
test_words = [x.split() for x in test_synopses_text]
LEN_TEST = len(test_words )
test_document_cat_probs = np.zeros(shape=(NUM_DIM, LEN_TEST), dtype=np.float)
for line_no in range(0,len(test_words)):
    for word in test_words[line_no]:
        if(word in sorted_dictionary_index):
            test_document_cat_probs[:,line_no] += word_wts[sorted_dictionary_index[word]]*prob_occurances_indoc_word[:,sorted_dictionary_index[word]]
test_document_cat_probs = test_document_cat_probs/np.sum(test_document_cat_probs,axis = 0)
np.savetxt("cleaned/test_document_cat_probs.txt", test_document_cat_probs.T, delimiter="|")


# np.save("cleaned/outputtrainmatrix", wordcount_doc )
