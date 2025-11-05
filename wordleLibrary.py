"""Functions necessary for our command line wordle game by Sam Selkregg"""
import random

"""Selects one random word from our wordlist file
   words.txt obtained from: tabatkins github wordle-list"""
def select_word(filename="words.txt"):
    with open(filename, "r") as file:
        words = file.read().splitlines()
    return random.choice(words)
    
"""Processes a guess by matching it to the word."""
def process_guess(word, guess):
    if len(word) != len(guess):
        return ""
    
    word = word.lower()
    guess = guess.lower()

    result = ["X"] * len(word)
    remainingLetters = list(word)

    ##Find the greens, remove them from our remaining word
    for i in range(len(word)):
        if guess[i]==word[i]:
            result[i]="G"
            remainingLetters[i]=None

    ##Find the yellows
    for i in range(len(word)):
        if result[i]=="G":
            continue
        if guess[i] in remainingLetters:
            result[i] = "Y"
            ##Remove one of the correct but wrong space letters from our list
            remainingLetters[remainingLetters.index(guess[i])] = None
    
    return "".join(result)

    





