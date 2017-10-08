rm(list=ls())

# -------------
# Load Libraries
# -------------
source("text_functions.R")
# -------------
# readfiles
# -------------
load("cleaned/testing_variants.bin")
load("cleaned/training_variants.bin")
load("cleaned/stage2_test_variants.bin")
# -------------
# Norvig word frequency list
# -------------
word_freq <- read.table("rawdata/word_frequencies.txt")
word_freq <- word_freq[1:30000,1]
word_freq <- as.character(word_freq)
# -------------
# Cleanup Testing Synopses
# -------------
synopses_input <- testing_variants$Synopsis
synopses <- cleaning_cancer_text(synopses_input,word_freq)
testing_variants$Synopsis <- synopses
save(testing_variants,file = "cleaned/testing_words_removed_cleaned.bin")
write(x = synopses,file = "cleaned/testing_synopses.txt")


# -------------
# Cleanup Training Synopses
# -------------
synopses_input <- training_variants$Synopsis
synopses <- cleaning_cancer_text(synopses_input,word_freq)
training_variants$Synopsis <- synopses
save(training_variants,file = "cleaned/training_words_removed_cleaned.bin")
write(x = synopses,file = "cleaned/training_synopses.txt")

# -------------
# Cleanup Training Synopses
# -------------
synopses_input <- stage2_test_variants$Synopsis
synopses <- cleaning_cancer_text(synopses_input,word_freq)
stage2_test_variants$Synopsis <- synopses
save(stage2_test_variants,file = "cleaned/stage2_test_words_removed_cleaned.bin")
write(x = synopses,file = "cleaned/stage2_test_synopses.txt")

