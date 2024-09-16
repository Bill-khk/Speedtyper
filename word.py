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


# Using Synchronous event listening instead of thread listening
def play2(word):
    with keyboard.Events() as events:
        current_letter = 0
        s_time = time.time()
        while current_letter != len(word):
            # Block at most one second
            event = events.get(10.0)
            if event is None:
                print('You did not press a key within ten second')
            else:
                pressed_letter = str(event.key)[1]
                if word[current_letter] == pressed_letter:
                    current_letter += 1

    e_time = time.time() - s_time
    print(f'typed in {e_time}')
    return (True, e_time)


# --------------------- Old listen function with thread listener -------------------------

# press_letter = ''
#
#
# def on_press(key):
#     global press_letter
#     try:
#         press_letter = key.char
#     except AttributeError:
#         print(f'Special key {key} pressed')
#
#
# # Define a function to handle key release events
# def on_release(key):
#     # print(f'Key {key} released')
#     return False
#
#
# def play(word):
#     current_letter = 0
#     s_time = time.time()
#     global press_letter
#     while current_letter != len(word):
#         # print(f'{current_letter}/{len(word)}')
#         with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#             listener.join()
#             if word[current_letter] == press_letter:
#                 current_letter += 1
#
#     e_time = time.time() - s_time
#     print(f'Typed in {e_time}')

# ---------------------------------------------------------------------------------------








