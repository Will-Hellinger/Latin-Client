import json
import os
import glob
from info import *
import nltk #used to tell if word is verb or noun
import inflect #best for verbs
import pyinflect #best for nouns


dict_path = f'.{subDirectory}data{subDirectory}'


def get_dictionary() -> dict:
    """
    Get the Latin-English dictionary.

    This function retrieves and constructs a Latin-English dictionary from JSON files located in the specified directory.

    :return: A dictionary containing Latin and English word mappings with morphology information.
    """

    dictionary = {}
    latin_dictionary = {}
    english_dictionary = {}

    file_list = []

    dictionary_directory_names = ['latin_dictionary', 'timed_vocabulary_dictionary']
    morphology_directory_names = ['timed_morphology_dictionary']

    for dictionary_name in dictionary_directory_names:
        file_list.extend(glob.glob(f'{dict_path}{dictionary_name}{subDirectory}*.json'))

    for file in file_list:
        temp_data = json.load(open(file, mode='r', encoding='utf-8'))
        english_words = []
        morph_values = []

        for item in temp_data:
            if temp_data[item] == True:
                english_words.append(item)
        
        latin_word = file.split(subDirectory)
        latin_word = latin_word[len(latin_word) - 1]

        for dictionary_name in morphology_directory_names:
            morph_dict = {}

            try:
                if os.path.exists(f'{dict_path}{dictionary_name}{subDirectory}{latin_word.lower()}'):
                    morph_dict = json.load(open(f'{dict_path}{dictionary_name}{subDirectory}{latin_word}', mode='r', encoding='utf-8'))

                if os.path.exists(f'{dict_path}{dictionary_name}{subDirectory}{latin_word}'):
                    morph_dict = json.load(open(f'{dict_path}{dictionary_name}{subDirectory}{latin_word}', mode='r', encoding='utf-8'))

                for morph_value in morph_dict:
                    if morph_dict[morph_value] == True:
                        morph_values.append(morph_value)
            except:
                morph_dict = {} # just in case file is broken

        latin_word = decode_file_name(latin_word).replace('.json', '')
        latin_word = latin_word.replace(',', '') #just in case

        latin_word = latin_word.lower()

        latin_dictionary[latin_word] = {"english" : english_words, "morphology" : morph_values}

        for english_word in english_words:
            english_word = english_word.lower()

            if english_dictionary.get(english_word) == None:
                english_dictionary[english_word] = [latin_word]
            
            elif item not in english_dictionary.get(english_word):
                latin_words = list(english_dictionary[english_word])

                if latin_word not in latin_words:
                    latin_words.append(latin_word)

                english_dictionary[english_word] = latin_words
    
    dictionary['english'] = english_dictionary
    dictionary['latin'] = latin_dictionary

    return dictionary


def convert_to_base(word: str) -> str:
    """
    Convert an English word to its base form.

    This function takes an English word, analyzes its part of speech (noun or verb), and converts it to its base form
    using linguistic libraries.

    :param word: The English word to be converted.
    :return: The base form of the English word.
    """

    if len(word.split(' ')) >= 2:
        word = word.split(' ')
    else:
        word = [word, '']
        
    temp = ''
    for a in range(len(word)):
        if word[a] == '':
            continue
        
        backup = word[a]
            
        try:
            word_type = nltk.pos_tag(nltk.word_tokenize(word[a]))[0][1]
            p = inflect.engine()

            if word_type.startswith("N") and p.singular_noun(word[a]) != False:
                word[a] = p.singular_noun(word[a])
            elif word_type.startswith("V") and pyinflect.getInflection(word[a], 'VB')[0] != False:
                word[a] = pyinflect.getInflection(word[a], 'VB')[0]

            if a != 0:
                temp += ' '
            
            temp += word[a]
        except:
            if a != 0:
                temp += ' '
            
            temp += backup

    return temp


def translate(word: str, language: str, dictionary: dict = get_dictionary(), use_base: bool = False) -> list:
    """
    Translate a word between Latin and English.

    This function translates a given word between Latin and English. It can use the base form of English words for
    improved translation accuracy.

    :param word: The word to be translated.
    :param language: The target language ('latin' or 'english') for translation.
    :param dictionary: The Latin-English dictionary.
    :param use_base: Whether to use the base form of English words for translation.
    :return: A list of translations for the input word in the target language.
    """

    language_dict = dictionary.get(language.lower())
    
    if language_dict is None:
        raise ValueError(f'Unsupported language: {language}')
    
    if use_base == True:
        word = convert_to_base(word)
    
    if word == "":
        return None
        
    return language_dict.get(word.lower())