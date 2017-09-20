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
load("cleaned/training_words_removed_cleaned.bin")
synopses <- readLines(con = "cleaned/training_synopses.txt")
# -------------
# readfiles
# -------------
