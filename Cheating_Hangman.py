#!/usr/bin/env python3
#COMP 3005 In Person
#Assignment 7
#Maya Fry 
from random import choice

def load_words(filename, length):
    """Takes in a text file, and a length, so that the function will pull all words in the
    text file of the same character length as the one provided, and creates a list of them.

    Args:
        filename (word file)): Text file of words, one word per row.
        length (int): The length of the words desired
        

    Returns:
        List: A list of words from a word file of the same length
    """
    try:
        with open(filename) as f:
            # get a list of all the words, but not including spaces, punctuation, etc
            return [i.strip().lower() for i in f if len(i.strip()) == length]
    except FileNotFoundError:
        print("File not found")
        return []

def test_load_words():
    if load_words("hangman_words_asldkfjaslkj.txt", 4) != []:
        print("Error with test_load_words.")

def input_size():
    """Prompts the user to pick a word size.

    Returns:
        Integrated Value: The desired word length to be used to start the game. 
    """
    while True:
        try:
            length = int(input("What word length? "))
            return length
        except:
            print("That isn't a number. ")

def mask_word(word, guessed):
    """Returns word with all letters not in guessed replaced with hyphens

    Args:
        word (str): the word to mask
        guessed (set): the guessed letters

    Returns:
        str: the masked word 
    """
    mask_word = ""
    for char in word:
        if char not in guessed:
            mask_word += "-"
        else:
            mask_word += char
    return mask_word

def test_mask_word():
    test1 = mask_word("zymurgy", {"y", "m"})
    test2 = mask_word("zigzagging", {"g", "i", "z"})
    test3 = mask_word("abcd", {"o", "e", "r"})
    test4 = mask_word("jiujitsu", {"a", "u", "r", "s"})
    test5 = mask_word("ivy", {})
    if test1 != "-ym---y":
        print(f"Error with test_mask_word. Zymurgy resulted in {test1}")
    if test2 != "zigz-ggi-g":
        print(f"Error with test_mask_word. Zigzagging resulted in {test2}")
    if test3 != "----":
        print(f"Error with test_mask_word. Abcd resulted in {test3}")
    if test4 != "--u---su":
        print(f"Error with test_mask_word. Jiujitsu resulted in {test4}")
    if test5 != "---":
        print(f"Error with test_mask_word. Ivy resulted in {test5}")        

def partition(words, guessed):
    """Generates the partitions of the set words based upon guessed

    Args:
        words (set): the word set
        guessed (set): the guessed letters

    Returns:
        dict: The partitions"""   
    partitions = {}
    for word in words:
        # First check to see if masked word is already in the dictionary
        # If so, add the word to the value set for that masked word
        if mask_word(word, guessed) in partitions:
            partitions[mask_word(word, guessed)].add(word)            
        # Otherwise make the masked word a key in the dictionary, and make the word the 
        # corresponding value
        else:
            partitions[mask_word(word, guessed)] = {word}  
    return partitions

def test_partition():
    test1 = partition(['jinx', 'onyx', 'quiz', 'shiv', 'wave', 'wavy', 'waxy'], {"w", "a", "o", "r"})
    test2 = partition(["abc", "abd", "abe", "abf", "abg"], {"a", "e", "b"})
    test3 = partition(["abcd", "abce", "abdg"], {"a", "b", "c"})
    if test1 != {'----': {'quiz', 'jinx', 'shiv'}, 'o---': {'onyx'}, 'wa--': {'wavy', 'waxy', 'wave'}}:
        print(f"Error with test_partition. Test1 resulted in {test1}")
    if test2 != {'ab-': {"abc", "abd", "abf", "abg"}, 'abe': {"abe"}}:
        print(f"Error with test_partition. Test2 resulted in {test2}")
    if test3 != {'abc-': {"abcd", "abce"}, 'ab--': {"abdg"}}:
        print(f"Error with test_partition. Test3 resulted in {test3}")

def max_partition(partitions):
    """Returns the hint for the largest partite set

    The maximum partite set is selected by selecting the partite set with
    1. The maximum size partite set
    2. If more than one maximum, prefer the hint with fewer revealed letters
    3. If there is still a tie, select randomly

    Args:
        partitions (dict): partitions from partition function

    Returns:
        str: hint for the largest partite set"""
    max_lst = []
    max_val = 0
    # Sift through all values in the dictionary, and determine the largest sized value set
    for i in partitions.values():
        if len(i) > max_val:
            max_lst = [i]
            max_val = len(i)
        elif len(i) == max_val:
            max_lst.append(i)
    # Now, if there is just one value set that has the largest size, pick that for the hint
    if len(max_lst) == 1:
        temphint = [key for key, value in partitions.items() if value == max_lst[0]]
        hint = " ".join(temphint)
        return hint
    # If there are multiple value sets of the same size, then see which value set
    # has a key with the most hyphens. 
    elif len(max_lst) > 1:
        key_lst = [key for key, value in partitions.items() if value in max_lst]
        max_hyp = 0
        hintList = []
        for i in key_lst:
            if i.count("-") > max_hyp:
                hintList = [i]
                max_hyp = i.count("-")
            elif i.count("-") == max_hyp:
                hintList.append(i)
        if len(hintList) > 1:
            # If all the keys have the same amount of hyphens, then choose randomly
            hint = choice(hintList)
        elif len(hintList) == 1:
            hint = hintList[0]  
        return hint   

def test_max_partition1():
    dict = {'i--ry': {'ivory'}, 'y----': {'yoked'}, '-i---': {'vixen', 'gizmo', 'pixel', 'kiosk', 'zilch'}, 'y---y': {'yummy'}, '-i--y': {'wimpy'}, '-a---': {'kazoo', 'banjo', 'waltz'}, '---i-': {'unzip', 'equip'}, '-y---': {'cycle', 'nymph', 'lymph'}, 'a--i-': {'affix'}, '-ai--': {'haiku'}, '--i--': {'blitz', 'quips'}, '-aya-': {'kayak'}, 'a-i--': {'axiom'}, '-ay--': {'bayou'}, '-a--y': {'jazzy', 'gabby'}, 'a----': {'askew'}, 'a-y--': {'abyss'}, '--y--': {'glyph'}, 'a--r-': {'azure'}, '----y': {'lucky', 'woozy', 'puppy', 'jelly', 'funny'}, '--a-i': {'khaki'}, '-----': {'klutz', 'queue', 'jumbo', 'buxom'}, '---a-': {'topaz', 'pshaw'}, '----a': {'polka', 'vodka'}, '--a--': {'staff'}, '--y-y': {'flyby'}, '--ary': {'ovary'}, '--i-y': {'juicy'}, '---r-': {'fjord'}, '-ry--': {'crypt'}}
    result = max_partition(dict)
    if result != "----y" and result != "-i---":
        print("Error with test_max_partition1.")
        print(f"Result is {result}")

def test_max_partition2():
    dict = {'abc-': {'abcd', 'abce'}, 'ab--': {'abdg', 'abdf'}}
    result = max_partition(dict)
    if result != "ab--":
        print("Error with test_max_partition2.")
        print(f"Result is {result}")

def test_max_partition3():
    dict = {'abc-': {'abcd', 'abce'}, 'abd-': {'abdg', 'abdf', 'abdj', 'abdk'}}
    result = max_partition(dict)
    if result != "abd-":
        print("Error with test_max_partition3.")
        print(f"Result is {result}")

def test_max_partition4():
    dict = {'abc-': {'abcd', 'abce', 'abcf', 'abcg'}, 'abd-': {'abdg', 'abdf', 'abdj', 'abdk'}, 'abe-': {'abea', 'abeb', 'abec', 'abed'}}
    result = max_partition(dict)
    if result != "abc-" and result != "abd-" and result != "abe-":
        print("Error with test_max_partition4.")
        print(f"Result is {result}")

def test_max_partition5():
    dict = {'----': {'abcd', 'abce', 'abcf', 'abcg', 'abdg', 'abdf', 'abdj'}}
    result = max_partition(dict)
    if result != "----":
        print("Error with test_max_partition5.")
        print(f"Result is {result}")
        
def test_max_partition():
    test_max_partition1()
    test_max_partition2()
    test_max_partition3()
    test_max_partition4()
    test_max_partition5()

def read_input(guesses):
    """Prompts the user to guess a letter for the game, and confirms that it is an acceptable guess.

    Args:
        guesses (set): Set of letters already guessed (will be empty when game starts)

    Returns:
        string: Guessed letter
    """
    while True:
        guess = input("Enter a letter: ").lower()
        if len(guess) != 1:
            print("Enter only one letter. ")
        elif not guess.isalpha():
            print("That isn't a letter. ")
        elif guess in guesses:
            print("You already guessed that. ")
        else:
            return guess

def game_over(guesses_remaining, hint):
    """Checks to see if the game is over according to two conditions:
    1. There are no more remaining guesses, and/or
    2. All the letters have been guessed in the hint

    Args:
        guesses_remaining (int): How many guesses are remaining for the user (max of 5)
        hint (string): the masked word from mask_word function

    Returns:
        boolean: True if one of the conditions are met (game is over), False otherwise
    """
    if guesses_remaining <= 0:
        return True
    if hint.count("-") == 0:
        return True
    return False 

def main():
    # Game setup
    length = input_size()
    cheat = length < 0 #Boolean type
    if cheat == True:
        length = length * -1
        words = load_words("hangman_words.txt", length)
    else:
        words = load_words("hangman_words.txt", length)
    if len(words) < 1:
        print("No words found of that length")
    if cheat == True:
        print(f"Potential words: {words}")
        print(f"There are {len(words)} potential words.")
    guesses_remaining = 5
    guesses = set()
    partitions = partition(words, guesses)
    hint = max_partition(partitions)
    # Game loop
    while not game_over(guesses_remaining, hint):
        # Print out game state
        print(f"You have {guesses_remaining} incorrect guesses remaining")
        print(f"Hint: {hint}")
        print(f"Guessed letters: {guesses}")
        # Get new input
        guess = read_input(guesses)
        guesses.add(guess)
        partitions = partition(words, guesses)
        if cheat == True:
            print(f"Partitions: {partitions}")
        next_hint = max_partition(partitions)
        if cheat == True:
            print(f"Chosen partition: {next_hint}")
        if hint != next_hint:
            # Correct guess
            print(f"Correct! {guess} is in the word.")
        else:
            print(f"I'm sorry, {guess} is not in the word.")
            guesses_remaining -= 1
        # Update game state
        words = partitions[next_hint]
        hint = next_hint

    # Game end conditions or end messages
    if hint.count("-") == 0:
        hintPartition = [list(value) for key, value in partitions.items() if key == hint]
        answer = choice(hintPartition[0])
        print(f"You win! The word was {answer}")
    else:
        hintPartition = [list(value) for key, value in partitions.items() if key == hint]
        answer = choice(hintPartition[0])
        print(f"You lose! The word was {answer}")

#test_load_words()
test_mask_word()
test_partition()
test_max_partition()
main()
