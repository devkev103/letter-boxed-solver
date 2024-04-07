import logging
from operator import itemgetter
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# user input of possible letters
sides = ["smh", 'ouy','tbd', 'aei']
possible_letters = "smhouydbtiea"
number_of_word_to_solve_in = 4

def load_words():
    with open('words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

def LettersInWord(word):
    letter_list = {}
    for char in set(word):
        letter_list[char]=word.count(char)
    return letter_list

def IsWordPossible(word: str, possible_letter_list: dict):
    is_word_possible = True

    if(len(word) <= 2):
        logging.debug(f"The word is too short to be valid: {word}")
        is_word_possible = False
        return is_word_possible

    word_letter_list = LettersInWord(word)

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

# english_words = load_words()
# possible_letter_list = LettersInWord(possible_letters)

# possible_english_words = FindPossibleWordsFromDict(english_words, possible_letter_list)
# possible_english_words = RemoveImpossibleWordsbySide(possible_english_words, sides)

# logging.info(sorted(possible_english_words))

a = ["kevin", 'niakds', 'sjkasdjf', 'side', 'emote', 'elotts']
# a = ["kevin", 'niakds', 'zjkasdjf', 'zide']

def recursion(max_chain_words: int, start_word: str, input_list: list, chain_list: list, sequences: list):
    if input_list == []:
        return
    
    input_list.remove(start_word)
    chain_list.append(start_word)

    if len(chain_list) >= max_chain_words:
        logger.info(f"chain_list: {chain_list}") # save this list
        sequences.append(chain_list[:])
        return
    
    new_list = [x for x in input_list if x[0] == start_word[-1]]
    logger.debug(f"new_list: {new_list}")

    if new_list == []:
        logger.debug("no more words")
        logger.info(f"chain_list: {chain_list}") # save this list
        sequences.append(chain_list[:])
        return

    for word in new_list:
        logger.debug(f"recusion with {word}, input_list: {input_list}")
        recursion(max_chain_words, word, input_list, chain_list, sequences)
        chain_list.pop()

    return

def rank_words(possible_letters: str, words: list) -> list:
    possible_letter_list = LettersInWord(possible_letters)
    ranked_words = []
    for word in words:
        word_letter_list = LettersInWord(word)
        common_keys = filter(lambda x: x in word_letter_list, possible_letter_list)
        key_count = 0
        for key in common_keys:
            key_count += 1
        ranked_words.append({"word": word, "rank": key_count})
    return ranked_words

def delete_word_from_dict(word: str, list: list):
    for i in range(len(list)):
        if list[i]['word'] == word:
            del list[i]
            break

# created a function just in case we want to create a more complex sorting function
def sort_rank_from_dict(list: list) -> list:
    return sorted(ranked_words, key=itemgetter('rank'), reverse=True)

sequences = []
recursion(4, 'kevin', a, [], sequences)

for sequence in sequences:
    print(sequence)

# recursion('thumbs', possible_english_words, [])
# ranked_words = rank_words('knfd', a)
# print(ranked_words)
# delete_word_from_dict('side', ranked_words)
# delete_word_from_dict('emote', ranked_words)
# print(ranked_words)
# print(sort_rank_from_dict(ranked_words))