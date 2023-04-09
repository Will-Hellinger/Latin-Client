import json
import os
from info import *

def get_dictionary():
    file_list = []
    dictionary = {}
    latin_dictionary = {}
    english_dictionary = {}

    for root, dirs, files in os.walk('.'):
        for file in files:
            if str(os.path.join(root,file)).endswith('.json') and ('latin_dictionary' in str(os.path.join(root,file) or 'timed_vocabulary_dictionary'in str(os.path.join(root,file)))):
                file_list.append(os.path.join(root,file))
    
    for file in file_list:
        temp_data = json.load(open(file, mode='r', encoding='utf-8'))
        temp_latin_values = []

        for item in temp_data:
            if temp_data[item] == True:
                temp_latin_values.append(item)
        
        latin_word = file.split(subDirectory)
        latin_word = latin_word[len(latin_word) - 1]
        latin_word = decodeFilename(latin_word).replace('.json', '')

        latin_dictionary[latin_word] = temp_latin_values
    
    for item in latin_dictionary:
        english_words = latin_dictionary[item]

        for english_word in english_words:

            if english_dictionary.get(english_word) == None:
                english_dictionary[english_word] = [item]

            elif item not in english_dictionary.get(english_word):
                latin_words = list(english_dictionary[english_word])
                latin_words.append(item)

                english_dictionary[english_word] = latin_words
    
    dictionary['english'] = english_dictionary
    dictionary['latin'] = latin_dictionary

    return dictionary


def translate(word: str, language: str, dictionary: dict = get_dictionary()):
    
    return dictionary[language.lower()].get(word)

def test_latin_output(words: str):
    latin_words = []
    word_list = words.split()
    
    for i in range(len(word_list)):
        for j in range(i+1, len(word_list)+1):
            combined_word = ''.join(word_list[i:j])
            if translate(combined_word, 'english') != None:
                latin_words.append(str(translate(combined_word, 'english')))
    
    if latin_words:
        print("Latin words found:", ', '.join(latin_words))
    else:
        print("No Latin words found.")

print(test_latin_output('They differ from each other in courage but surpass the rest of the Germans in greed.'))