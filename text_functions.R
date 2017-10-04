
cleaning_cancer_text <- function(synopses,frequent_words){
  frequent_words <- as.character(frequent_words)
  frequent_words <-tolower(frequent_words)
  # Convert to lower
  synopses <-tolower(synopses)
  
  # Loop with 14 gsubs as gsub doesn't accept 30k long sequence
  i=0
  for(i in 0:14){
    a <- paste0("\\b(",paste(frequent_words[(i*2000+1):(i*2000+2000)],collapse = "|"),")\\b")
    synopses <- gsub(pattern = a,replacement = " ",x = synopses,perl = T)
    print(i)
  }
  
  rm(i,a)
  # -------------
  # Clean after removing words - training
  # -------------
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
  return(synopses)
}