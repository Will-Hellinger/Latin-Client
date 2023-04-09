import custom_translator
from web_driver import *
from info import *

def solve():
    parentElement = driver.find_element(By.CLASS_NAME, 'ui-block-a')
    english_texts = parentElement.find_elements(By.XPATH, "// p[@style='white-space:pre-wrap;margin-right:2em;font-size:1em']")
    latin_inputs = parentElement.find_elements(By.CLASS_NAME, 'latin composition ui-input-text ui-shadow-inset ui-body-inherit ui-corner-all ui-textinput-autogrow')
    dictionary = custom_translator.get_dictionary()

    all_inputs = []

    for english_text in english_texts:
        english_text = english_text.text
        english_text = english_text.split(' ')

        inputs = []

        for i in range(len(english_text)):
            for j in range(i+1, len(english_text)+1):
                combined_word = ''.join(english_text[i:j])

                output = custom_translator.translate(combined_word, 'english', dictionary)

                if output != None:
                    inputs.append(output)
        
        
        all_inputs.append(inputs)