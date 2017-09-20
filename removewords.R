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
# Read English Dictionaries
# -------------


# Norvig by frequency
word_freq <- read.table("rawdata/word_frequencies.txt")
word_freq <- word_freq[1:30000,1]
word_freq <- as.character(word_freq)
word_freq <-tolower(word_freq)
write(word_freq,file="rawdata/words_to_remove.csv")

# -------------
# Remove EnglishWords from text - training
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

rm(i,a)
# -------------
# Clean after removing words - training
# -------------
# rm(list=ls())
# load("cleaned/training_words_removed.bin")
synopses <- training_variants$Synopsis
synopses <- iconv(synopses, "latin1", "ASCII", sub="")
synopses <- gsub("[[0-9]+]"," ",synopses)
synopses <- gsub("\\([0-9]+\\)"," ",synopses)
synopses <- gsub("\\([0-9]+\\, [0-9]+\\)"," ",synopses)
synopses <- gsub("\\([0-9]+\\, [0-9]+\\, [0-9]+\\)"," ",synopses)
synopses <- gsub("\\([0-9]+\\, [0-9]+\\, [0-9]+\\, [0-9]+\\)"," ",synopses)
synopses <- gsub("[[:punct:]]", "", synopses)
synopses <- gsub(" [0-9] "," ",synopses)
synopses <- gsub(" [0-9][0-9] "," ",synopses)
synopses <- gsub(pattern = " +"," ", synopses)
synopses <- gsub(pattern = "^ ","", synopses)
synopses <- gsub(pattern = " $","", synopses)
training_variants$Synopsis <- synopses
save(training_variants,file = "cleaned/training_words_removed_cleaned.bin")

write(x = synopses,file = "cleaned/training_synopses.txt")

# -------------
# Remove EnglishWords from text - testing
# -------------
synopses <- as.character(testing_variants$Synopsis)
synopses <-tolower(synopses)

i=0
for(i in 0:14){
  a <- paste0("\\b(",paste(word_freq[(i*2000+1):(i*2000+2000)],collapse = "|"),")\\b")
  synopses <- gsub(pattern = a,replacement = " ",x = synopses,perl = T)
  print(i)
}
testing_variants$Synopsis <- synopses
save(testing_variants,file = "cleaned/testing_words_removed.bin")

rm(i,a,synopses)



# -------------
# Clean after removing words - testing
# -------------
# rm(list=ls())
# load("cleaned/testing_words_removed.bin")
synopses <- testing_variants$Synopsis
synopses <- iconv(synopses, "latin1", "ASCII", sub="")
synopses <- gsub("[[0-9]+]"," ",synopses)
synopses <- gsub("\\([0-9]+\\)"," ",synopses)
synopses <- gsub("\\([0-9]+\\, [0-9]+\\)"," ",synopses)
synopses <- gsub("\\([0-9]+\\, [0-9]+\\, [0-9]+\\)"," ",synopses)
synopses <- gsub("\\([0-9]+\\, [0-9]+\\, [0-9]+\\, [0-9]+\\)"," ",synopses)
synopses <- gsub("[[:punct:]]", "", synopses)
synopses <- gsub(" [0-9] "," ",synopses)
synopses <- gsub(" [0-9][0-9] "," ",synopses)
synopses <- gsub(pattern = " +"," ", synopses)
synopses <- gsub(pattern = "^ ","", synopses)
synopses <- gsub(pattern = " $","", synopses)
testing_variants$Synopsis <- synopses
save(testing_variants,file = "cleaned/testing_words_removed_cleaned.bin")

write(x = synopses,file = "cleaned/testing_synopses.txt")


