import json
import os
from info import *
import nltk #used to tell if word is verb or noun
import inflect #best for verbs
import pyinflect #best for nouns

def get_dictionary():
    file_list = []
    dictionary = {}
    latin_dictionary = {}
    english_dictionary = {}

    for root, dirs, files in os.walk('.'):
        for file in files:
            if str(os.path.join(root,file)).endswith('.json') and ('latin_dictionary' in str(os.path.join(root,file)) or 'temp_latin_dictionary'in str(os.path.join(root,file)) or 'timed_vocabulary_dictionary'in str(os.path.join(root,file))):
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
        latin_word = latin_word.replace(',', '') #just in case

        latin_word = latin_word.lower()

        latin_dictionary[latin_word] = temp_latin_values
    
    for item in latin_dictionary:
        english_words = latin_dictionary[item]

        for english_word in english_words:

            english_word = english_word.lower()

            if english_dictionary.get(english_word) == None:
                english_dictionary[english_word] = [item]

            elif item not in english_dictionary.get(english_word):
                latin_words = list(english_dictionary[english_word])
                latin_words.append(item)

                english_dictionary[english_word] = latin_words
    
    dictionary['english'] = english_dictionary
    dictionary['latin'] = latin_dictionary

    return dictionary


def convert_to_base(word):
    backup = word

    try:
        if len(word.split(' ')) >= 2:
            word = word.split(' ')
        else:
            word = [word, '']
        
        temp = ''
        for a in range(len(word)):
            if word[a] == '':
                continue
            
            word_type = nltk.pos_tag(nltk.word_tokenize(word[a]))[0][1]
            p = inflect.engine()

            if word_type.startswith("N") and p.singular_noun(word[a]) != False:
                word[a] = p.singular_noun(word[a])
            elif word_type.startswith("V") and pyinflect.getInflection(word[a], 'VB')[0] != False:
                word[a] = pyinflect.getInflection(word[a], 'VB')[0]

            if a != 0:
                temp += ' '
            
            temp += word[a]
        
        word = temp
    except:
        word = backup

    return word


def translate(word: str, language: str, dictionary: dict = get_dictionary(), use_base = False):
    language_dict = dictionary.get(language.lower())
    
    if language_dict is None:
        raise ValueError(f'Unsupported language: {language}')
    
    if use_base == True:
        word = convert_to_base(word)
        
    return language_dict.get(word.lower())