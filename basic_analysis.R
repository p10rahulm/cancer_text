rm(list=ls())
# -------------
# Load Libraries
# -------------
library(stringr)

# -------------
# readfiles
# -------------

testing_variants <- read.csv("rawdata/test_variants.csv")
training_variants <- read.csv("rawdata/training_variants.csv")

# -------------
# Extending testing_variants
# -------------
testing_textvec <- readLines("rawdata/test_text")
testing_textvec <- testing_textvec[2:length(testing_textvec)]
testing_textvec <- gsub(pattern = "[0-9]+\\|\\|",replacement = "",testing_textvec)

testing_text <- data.frame("ID"=seq(0,length(testing_textvec)-1),"Synopsis" = testing_textvec)
testing_variants <- merge(testing_variants,testing_text,by.x="ID",by.y = "ID",all.x=T)
rm(testing_text,testing_textvec)
save(testing_variants,file = "cleaned/testing_variants.bin")
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


# -------------
# Extending stage2_variants
# -------------
stage2_test_variants <- read.csv("rawdata/stage2_test_variants.csv")


stage2_test_textvec <- readLines("rawdata/stage2_test_text.csv")
stage2_test_textvec <- stage2_test_textvec[2:length(stage2_test_textvec)]
stage2_test_textvec <- gsub(pattern = "[0-9]+\\|\\|",replacement = "",stage2_test_textvec)

stage2_test_text <- data.frame("ID"=seq(0,length(stage2_test_textvec)-1),"Synopsis" = stage2_test_textvec)
stage2_test_variants <- merge(stage2_test_variants,stage2_test_text,by.x="ID",by.y = "ID",all.x=T)
rm(stage2_test_text,stage2_test_textvec)
save(stage2_test_variants,file = "cleaned/stage2_test_variants.bin")

