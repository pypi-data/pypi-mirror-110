from os import getcwd
import json
from random import choice
from PyDictionary import PyDictionary


def get_info(word):
    dictionary = PyDictionary()
    
    # gets synonyms
    synonyms_list = dictionary.synonym(word)
    synonyms = ""
    for synonym in synonyms_list[3:5]:
        synonyms += (synonym + ", ")
    
    # get antonyms
    antonyms_list = dictionary.antonym(word)
    antonyms = ""
    for antonym in antonyms_list[3:5]:
        antonyms += (antonym + ", ")

    return "Synonyms: "+ synonyms + "\n\n" + "Antonyms: " + antonyms
def get_word(path):
    words_data = open(path, "r")
    words = words_data.read().split("\n")
    random_word = choice(words)
    return random_word

def get_path():
    working_dir_path = getcwd().replace("\\", "\\\\")
    full_path = working_dir_path + "\\notify_vocab\\assets\\words.txt" # replace it with your path

    return full_path

path = get_path()
random_word = get_word(path)
info = get_info(random_word)
    
    

    
    