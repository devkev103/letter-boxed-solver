import logging
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

english_words = load_words()
possible_letter_list = LettersInWord(possible_letters)

possible_english_words = FindPossibleWordsFromDict(english_words, possible_letter_list)
possible_english_words = RemoveImpossibleWordsbySide(possible_english_words, sides)

logging.info(sorted(possible_english_words))