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

    dictionary_directory_names = ['latin_dictionary', 'timed_vocabulary_dictionary']
    morphology_directory_names = ['timed_morphology_dictionary']

    file_list = [file for dictionary_name in dictionary_directory_names for file in glob.glob(f'{dict_path}{dictionary_name}{subDirectory}*.json')]

    for file in file_list:
        with open(file, mode='r', encoding='utf-8') as f:
            temp_data = json.load(f)
        english_words = [item for item in temp_data if temp_data[item]]

        latin_word = file.split(subDirectory)[-1]

        for dictionary_name in morphology_directory_names:
            morph_dict = {}
            
            try:
                morph_file_path = f'{dict_path}{dictionary_name}{subDirectory}{latin_word.lower()}'

                if os.path.exists(morph_file_path):
                    with open(morph_file_path, mode='r', encoding='utf-8') as f:
                        morph_dict = json.load(f)

                morph_values = [morph_value for morph_value in morph_dict if morph_dict[morph_value]]
            except:
                morph_dict = {} # just in case file is broken

        latin_word = decode_file_name(latin_word).replace('.json', '').replace(',', '').lower()

        latin_dictionary[latin_word] = {"english" : english_words, "morphology" : morph_values}

        for english_word in english_words:
            english_word = english_word.lower()
            english_dictionary.setdefault(english_word, [])

            if latin_word not in english_dictionary[english_word]:
                english_dictionary[english_word].append(latin_word)
    
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
    p = inflect.engine()
    words = word.split(' ')
    base_words = []

    for word in words:
        if word == '':
            continue

        try:
            word_type = nltk.pos_tag(nltk.word_tokenize(word))[0][1]

            if word_type.startswith("N") and p.singular_noun(word) is not False:
                word = p.singular_noun(word)
            elif word_type.startswith("V") and pyinflect.getInflection(word, 'VB')[0] is not False:
                word = pyinflect.getInflection(word, 'VB')[0]

            base_words.append(word)
        except:
            base_words.append(word)

    return ' '.join(base_words)


def translate(word: str, language: str, dictionary: dict = get_dictionary(), use_base: bool = False) -> list:
    """
    Translate a word between Latin and English.

    This function translates a given word between Latin and English. It can use the base form of English words for
    improved translation accuracy.

    :param word: The word to be translated.
    :param language: The starting language ('latin' or 'english') for translation.
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