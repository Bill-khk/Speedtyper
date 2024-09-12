import json, random
import time

from pynput import keyboard


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


def type_word(wList):
    selected_word = select_random(wList)
    print(selected_word)


# Define a function to handle key press events
press_letter = ''


def on_press(key):
    global press_letter
    try:
        press_letter = key.char
    except AttributeError:
        print(f'Special key {key} pressed')


# Define a function to handle key release events
def on_release(key):
    # print(f'Key {key} released')
    return False


def play(word):
    current_letter = 0
    s_time = time.time()
    global press_letter
    while current_letter != len(word):
        # print(f'{current_letter}/{len(word)}')
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
            if word[current_letter] == press_letter:
                current_letter += 1

    e_time = time.time() - s_time
    print(f'typed in {e_time}')


# ---------------------- Main---------------------
test_list = extract_json_word(5, 'words/words_dictionary.json')
test = select_random(test_list)
print(test)
play(test)
