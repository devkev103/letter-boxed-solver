# Letter Box Solver #

This program solves [Letter Boxed](https://www.nytimes.com/puzzles/letter-boxed)

`words_alpha.txt` came from [this](https://github.com/dwyl/english-words/tree/master?tab=readme-ov-file) repo.

## How to Use ##

1. Execute `remove_word_from_dictionary.py`
   1. This generates `curated_words.txt` by removing invalid words from `words_alpha.txt`
2. Exeute `letter_box_solver.py` with user input

## Known Issues ##

Not all words in `word_alpha.txt` are valid in the Letter Boxed game. `invalid_words.txt` is used to remove these invalid words from `words_alpha.txt` to generate `curated_words.txt`. All words in `invalid_words.txt` should be lowercase.

Removing a word from the input_list removes it from consideration going forward. This causes there to be different final sequences each run.