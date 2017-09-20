# -------------
# Clean after removing words
# -------------
rm(list=ls())
load("cleaned/training_words_removed.bin")
synopses <- training_variants$Synopsis
synopses <- iconv(synopses, "latin1", "ASCII", sub="")
synopses <- gsub("[[0-9]+]"," ",synopses)
synopses <- gsub("\\([0-9]+\\)"," ",synopses)
synopses <- gsub("\\([0-9]+\\, [0-9]+\\)"," ",synopses)
synopses <- gsub("\\([0-9]+\\, [0-9]+\\, [0-9]+\\)"," ",synopses)
synopses <- gsub("\\([0-9]+\\, [0-9]+\\, [0-9]+\\, [0-9]+\\)"," ",synopses)
synopses <- gsub("[[:punct:]]", "", synopses)
synopses <- gsub(" [0-9][0-9] "," ",synopses)
synopses <- gsub(pattern = " +"," ", synopses)
synopses <- gsub(pattern = "^ ","", synopses)
synopses <- gsub(pattern = " $","", synopses)
training_variants$Synopsis <- synopses
save(training_variants,file = "cleaned/training_words_removed_cleaned.bin")

write(x = synopses,file = "cleaned/training_synopses.txt")