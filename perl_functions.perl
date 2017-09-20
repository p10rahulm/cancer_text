perl -Mopen=locale -Mutf8 -lpe 'BEGIN{open(A,"eng_dictionary.txt"); chomp(@k = <A>)} for $w (@k){s/(^|[ ,.—_;-])\Q$w\E([ ,.—_;-]|$)/$1$2/ig}' training_text_edit_trial.txt 


perl -lpe 'BEGIN{open(A,"words_to_remove_subset.csv"); chomp(@k = <A>)} for $w (@k){s/\b\Q$w\E\b//ig}' training_text_edit_trial.txt > output_training_text_edit_trial.txt


