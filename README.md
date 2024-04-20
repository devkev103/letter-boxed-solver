# Letter Boxed Solver #

This program solves NYT's [Letter Boxed](https://www.nytimes.com/puzzles/letter-boxed)

`words_alpha.txt` came from [this](https://github.com/dwyl/english-words/tree/master?tab=readme-ov-file) repo.

## How to Use ##

1. Execute `remove_word_from_dictionary.py`
   1. This generates `curated_words.txt` by removing invalid words from `words_alpha.txt`
2. Execute `letter_boxed_solver.py` with user input

## Known Issues ##

As I don't know which words are valid for the Letter Boxed game, many sequences generated will be invalid. Thus, not all words in `word_alpha.txt` are valid in the Letter Boxed game. `invalid_words.txt` is used to remove these invalid words from `words_alpha.txt` to generate `curated_words.txt`. All words in `invalid_words.txt` should be lowercase.

During the recursion part of the solver, removing a word from the input_list removes it from consideration going forward. This causes there to be different final sequences for each run.

## TODO ##

- Clean code further and speed up the slowness