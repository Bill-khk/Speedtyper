import json
import random
import time
from pynput import keyboard


class Word:

    def __init__(self):
        pass


# ---------------Retrieve Data and format -------------------------
# Extract only the 5+ letter words in a list
def extract_json_word(nLetter, file):
    with open(file, 'r') as data_file:
        data = json.load(data_file)
    filtered_list = []
    for keys in data:
        if len(keys) >= nLetter:
            filtered_list.append(keys)
    return filtered_list


# select a random word in a list
def select_random(wList):
    return wList[random.randint(0, len(wList))]
