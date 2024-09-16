import word


# ---------------------- Main---------------------
test_list = word.extract_json_word(5, 'words/words_dictionary.json')
test = word.select_random(test_list)
print(test)
word.play2(test)
