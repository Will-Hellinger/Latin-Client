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
    
    for latin_input in latin_inputs:
        default_color = 'red'
        answers = []

        if str(latin_input.get_attribute('style')) != 'color:red;white-space:pre-wrap;margin-right:2em;padding:3%':
            default_color = 'green'
        
        span_texts = latin_input.find_elements(By.TAG_NAME, 'span')
        text = latin_input.text

        if default_color == 'green' and len(span_texts) == 0:
            answers.extend(text.split(' '))

        elif default_color == 'green' and len(span_texts) != 0:
            for span_text in span_texts:
                if 'red' in str(span_text.get_attribute('style')):
                    text.replace(span_text.text, '')
            
            answers.extend(text.split(' '))
        
        elif default_color == 'red' and len(span_texts) != 0:
            temp_answers = []
            for span_text in span_texts:
                if 'green' in str(span_text.get_attribute('style')):
                    temp_answers.append(span_text.text)
                
            answers.extend(temp_answers)

        print(answers)

    question = 1
    for input in all_inputs:
        print(f'{question}. {input}\n\n')
        question += 1