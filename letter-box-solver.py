import logging
from operator import itemgetter
import random
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# user input of possible letters
sides = ["pal", 'ons','uti', 'dry']
number_of_word_to_solve_in = 4
# user can enter a possible starting word and see if it can be solved from that
# left empty, we will use the best five starting words
starter_word = 'supinator'
shuffle_final_sequences = False

def load_words():
    with open('curated_words.txt') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

def get_letters_in_word(word: str) -> dict:
    letter_dict = {}
    for char in set(word):
        letter_dict[char]=word.count(char)
    return letter_dict

def IsWordPossible(word: str, possible_letter_list: dict):
    is_word_possible = True

    if(len(word) <= 2):
        logging.debug(f"The word is too short to be valid: {word}")
        is_word_possible = False
        return is_word_possible

    word_letter_list = get_letters_in_word(word)

    # time complexity: O(n) where n is the total number of items in both dictionaries.
    # Auxiliary space: O(1)
    common_keys = filter(lambda x: x in word_letter_list, possible_letter_list)
    key_count = 0
    for key in common_keys:
        key_count += 1 
        if (word_letter_list[key] > possible_letter_list[key]):
            logging.debug(f"the number of {key} is not possible")
            is_word_possible = False
            return is_word_possible

    if (key_count != len(word_letter_list)):
        logging.debug("the length of lists do not match")
        is_word_possible = False
        return is_word_possible

    return is_word_possible

def FindPossibleWordsFromDict(dictionary, possible_letter_list: dict):
    possible_english_words = []
    
    for word in dictionary:
        if (IsWordPossible(word, possible_letter_list)):
            logging.debug(f"The word is possible: {word}")
            possible_english_words.append(word)
        # else:
            logging.debug(f"The word is NOT possible: {word}")

    logging.debug(possible_english_words)
    return possible_english_words

def IsWordPossibleSide(word: str, side: str) -> bool:
    logging.debug(f"The word is {word} and side is {side}")
    for i in range(0, len(word) - 1):
        current_letter = word[i]
        if i < len(word) - 1:
            next_letter = word[i+1]
        if current_letter in side and next_letter in side:
            logging.debug(f"The word {word} is not possible given the side {side}")
            return False
    return True

def RemoveImpossibleWordsbySide(words: str, sides: str) -> list:
    for word in reversed(words):
        for side in sides:
            if(not IsWordPossibleSide(word, side)): 
                logging.debug(f"remove {word}")
                possible_english_words.remove(word)
                break
    return words

def find_all_sequences_recursion(max_chain_words: int, match_letters: dict, start_word: str, input_list: dict, chain_list: list, sequences: list):
    # list has been exhausted; return
    if input_list == []:
        return
    
    logger.debug(f"removing start_word: {start_word}")
    if start_word in input_list:
        input_list.remove(start_word)

    logger.debug(f"appending start_word to chain_list: {start_word}")
    chain_list.append(start_word)

    # case when chain_list is completed early ie has all necessary letters
    if (is_sequence_complete(chain_list, match_letters)):
        logger.debug(f"chain list completed early; chain list complete: {chain_list}")
        sequences.append(chain_list[:])
        return

    # max amount of words has been reached; 
    # check if sequence is complete ie contains all the necessary letters
    # if complete, add current sequence chain
    if len(chain_list) >= max_chain_words:
        if (is_sequence_complete(chain_list, match_letters)):
            logger.debug(f"reached max chain words; chain list complete: {chain_list}")
            sequences.append(chain_list[:])
        else:
            logger.debug(f"reached max chain words; chain list NOT complete: {chain_list}")
        return
    
    # find all matches with the last letter of start_word (start_word[-1])
    # and the first letter of the remainder input_list (x['word'][0])
    # new_list = [x for x in word_bank if x['word'][0]== start_word[-1]]
    preferred_letters = get_unmatched_sequence_letters(get_letters_in_word(match_letters), chain_list)
    ranks = rank_and_sort_words(match_letters, possible_english_words, preferred_letters.keys())
    new_list = [x['word'] for x in ranks if x['word'][0] == start_word[-1]]
    # new_list = [x for x in input_list if x[0]== start_word[-1]]
    logger.debug(f"new_list: {new_list}")

    # no more match end to start letter matches
    # check if sequence is complete ie contains all the necessary letters
    # if complete, add current sequence chain
    if new_list == []:
        if (is_sequence_complete(chain_list, match_letters)):
            logger.debug(f"no more words in new_list; chain list complete: {chain_list}")
            sequences.append(chain_list[:])
        else:
            logger.debug(f"no more words in new_list; chain_list is NOT complete: {chain_list}")
        return

    for word in new_list:
        logger.debug(f"recusion with {word}, input_list: {input_list}")
        find_all_sequences_recursion(max_chain_words, match_letters, word, input_list, chain_list, sequences)
        if len(chain_list) > 0:
            chain_list.pop() # remove last word in chain as that word is now done.

    return

def rank_and_sort_words(match_letters: dict, words: list, preferred_letters: list ) -> list:
    ranked_words = []
    for word in words:
        word_letter_list = get_letters_in_word(word)
        common_keys = filter(lambda x: x in word_letter_list, match_letters)
        key_count = 0
        for key in common_keys:
            key_count += 1
            if key in preferred_letters:
                key_count += 10
        ranked_words.append({"word": word, "rank": key_count})
    return sorted(ranked_words, key=itemgetter('rank'), reverse=True)

def delete_word_from_dict(word: str, list: list):
    for i in range(len(list)):
        if list[i]['word'] == word:
            del list[i]
            break

def is_sequence_complete(sequence: list, match_letter_list: dict) -> bool:
    sequence_letter_list = get_letters_in_word("".join(sequence))
    common_keys = filter(lambda x: x in sequence_letter_list, match_letter_list)
    key_count = 0
    for key in common_keys:
        key_count += 1

    if key_count == len(match_letter_list):
        return True
    else:
        return False

def get_unmatched_sequence_letters(match_letter_list: dict, sequnece: list) -> dict:
    sequence_letter_list = get_letters_in_word("".join(sequnece))
    mismatch = match_letter_list.keys() - sequence_letter_list.keys()
    remainder = "".join(mismatch)
    return get_letters_in_word(remainder)

## TEST DRIVER CODE ##
# tart_word = 'kevin'
# match_letters = get_letters_in_word('poekn')
# word_bank = ["kevin", 'niakds', 'sjkasdjf', 'side', 'emote', 'elotts', 'side']
# word_bank = rank_and_sort_words(match_letters, word_bank)
# get_unmatched_sequence_letters(match_letters, word_bank)
# for word in word_bank:
# find_all_sequences_recursion(5, match_letters, start_word, word_bank, [], sequences)

## DRIVER CODE ##
match_letters = "".join(sides)
match_letter_list = get_letters_in_word(match_letters)

english_words = load_words()
possible_english_words = FindPossibleWordsFromDict(english_words, match_letter_list)
possible_english_words = RemoveImpossibleWordsbySide(possible_english_words, sides)

# get top ten words
starter_words = []
if starter_word == '':
    starter_words = rank_and_sort_words(match_letter_list, possible_english_words, [])[:5]
else:
    starter_words.append({"word": starter_word})

for starter_word in starter_words:
    sequences = []
    word_list = possible_english_words[:]
    find_all_sequences_recursion(max_chain_words=number_of_word_to_solve_in, 
                                match_letters=match_letters, 
                                start_word=starter_word['word'], 
                                input_list=word_list, 
                                chain_list=[], 
                                sequences=sequences)

    if sequences == []:
        logger.info(f"no sequences found that has all match_letters for starter word: {starter_word}")
    else:
        logger.info(f"Showing top 100 sequnces found for starter_word: {starter_word} ({len(sequences)})")
        if (shuffle_final_sequences): 
            random.shuffle(sequences)
        for sequence in sequences[:100]:
            logger.info(sequence)