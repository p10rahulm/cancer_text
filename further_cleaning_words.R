# -------------
# Remove All EnglishWords from text
# -------------
# All english words
# Below seems excessive removal. Not going ahead at present
engwords <- readLines("rawdata/eng_dictionary.txt")
engwords <-tolower(engwords)

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