rm(list=ls())

# -------------
# Load Libraries
# -------------
library(stringr)
library(tm)
# install.packages("RWeka")
library(RWeka)
library(SnowballC)

# -------------
# readfiles
# -------------
load("cleaned/test_variants.bin")
load("cleaned/training_variants.bin")

# -------------
# Read English Dictionaries
# -------------

# All english words
engwords <- readLines("rawdata/eng_dictionary.txt")
engwords <-tolower(engwords)
# Norvig by frequency
word_freq <- read.table("rawdata/word_frequencies.txt")
word_freq <- word_freq[1:30000,1]
word_freq <- as.character(word_freq)
word_freq <-tolower(word_freq)
# word_freq <- gsub(pattern = "^",replacement = " ",x = word_freq,perl = T)
# word_freq <- gsub(pattern = "$",replacement = " ",x = word_freq,perl = T)
write(word_freq,file="rawdata/words_to_remove.csv")
word_freq_subset <- word_freq[1:100]
write(word_freq_subset,file="rawdata/words_to_remove_subset.csv")
# -------------
# Remove EnglishWords from text
# -------------
synopses <- as.character(training_variants$Synopsis)
synopses <-tolower(synopses)

i=0
for(i in 0:14){
  a <- paste0("\\b(",paste(word_freq[(i*2000+1):(i*2000+2000)],collapse = "|"),")\\b")
  synopses <- gsub(pattern = a,replacement = " ",x = synopses,perl = T)
  print(i)
}
training_variants$Synopsis <- synopses
save(training_variants,file = "cleaned/training_words_removed.bin")

rm(i,a,synopses)

# -------------
# Remove All EnglishWords from text
# -------------
synopses <- as.character(training_variants$Synopsis)
synopses <-tolower(synopses)

i=0
for(i in 0:465){
  a <- paste0("\\b(",paste(engwords[(i*1000+1):(i*1000+1000)],collapse = "|"),")\\b")
  synopses <- gsub(pattern = a,replacement = " ",x = synopses,perl = T)
  print(i)
}
training_variants$Synopsis <- synopses
save(training_variants,file = "cleaned/training_all_words_removed.bin")
