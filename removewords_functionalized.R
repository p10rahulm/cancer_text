rm(list=ls())

# -------------
# Load Libraries
# -------------

# -------------
# readfiles
# -------------
load("cleaned/test_variants.bin")
load("cleaned/training_variants.bin")

# -------------
# Cleanup Testing Synopses
# -------------
synopses <- cleaning_cancer_text(testing_variants$synopses)
testing_variants$Synopsis <- synopses
save(testing_variants,file = "cleaned/testing_words_removed_cleaned.bin")
write(x = synopses,file = "cleaned/testing_synopses.txt")


# -------------
# Cleanup Training Synopses
# -------------
synopses <- cleaning_cancer_text(training_variants$synopses)
training_variants$Synopsis <- synopses
save(training_variants,file = "cleaned/training_words_removed_cleaned.bin")
write(x = synopses,file = "cleaned/training_synopses.txt")

