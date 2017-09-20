rm(list=ls())
# -------------
# Load Libraries
# -------------
library(stringr)

# -------------
# readfiles
# -------------

test_variants <- read.csv("rawdata/test_variants.csv")
training_variants <- read.csv("rawdata/training_variants.csv")

# -------------
# Extending test_variants
# -------------
test_textvec <- readLines("rawdata/test_text")
test_textvec <- test_textvec[2:length(test_textvec)]
test_textvec <- gsub(pattern = "[0-9]+\\|\\|",replacement = "",test_textvec)

test_text <- data.frame("ID"=seq(0,length(test_textvec)-1),"Synopsis" = test_textvec)
test_variants <- merge(test_variants,test_text,by.x="ID",by.y = "ID",all.x=T)
rm(test_text,test_textvec)
save(test_variants,file = "cleaned/test_variants.bin")
# -------------
# Extending training_variants
# -------------

training_textvec <- readLines("rawdata/training_text")
training_textvec <- training_textvec[2:length(training_textvec)]
training_textvec <- gsub(pattern = "[0-9]+\\|\\|",replacement = "",training_textvec)

training_text <- data.frame("ID"=seq(0,length(training_textvec)-1),"Synopsis" = training_textvec)
training_variants <- merge(training_variants,training_text,by.x="ID",by.y = "ID",all.x=T)
rm(training_text,training_textvec)
save(training_variants,file = "cleaned/training_variants.bin")



