import custom_translator
from web_driver import *
import time
import unicodedata
from info import *


def strip_accents(text):
    return str(''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')).lower()


def solve():
    parentElement = driver.find_element(By.CLASS_NAME, 'ui-block-a')
    english_texts = parentElement.find_elements(By.XPATH, "// p[@style='white-space:pre-wrap;margin-right:2em;font-size:1em']")
    latin_inputs = parentElement.find_elements(By.XPATH, "// div[@class='latin composition ui-input-text ui-shadow-inset ui-body-inherit ui-corner-all ui-textinput-autogrow']")
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
    all_answers = []

    for latin_input in latin_inputs:
        driver.execute_script("arguments[0].scrollIntoView();", latin_input)
        default_color = 'green'
        answers = []

        if 'color:red' in str(latin_input.get_attribute('style')).replace(' ', ''):
            default_color = 'red'
        
        span_texts = latin_input.find_elements(By.TAG_NAME, 'span')
        text = latin_input.text

        if default_color == 'green' and len(span_texts) == 0:
            text = text.lower()
            answers.extend(text.split(' '))

        elif default_color == 'green' and len(span_texts) != 0:
            for span_text in span_texts:
                if 'red' in str(span_text.get_attribute('style')):
                    text.replace(span_text.text, '')
            
            text = text.lower()
            
            answers.extend(text.split(' '))
        
        elif default_color == 'red' and len(span_texts) != 0:
            temp_answers = []
            for span_text in span_texts:
                if 'green' in str(span_text.get_attribute('style')) or 'rgb(255,255,255)' in str(span_text.get_attribute('style')).replace(' ', ''):
                    temp_answers.append(str(span_text.text).lower())
                
            answers.extend(temp_answers)

        all_answers.append(answers)


    for a in range(0, len(all_inputs)):
        for b in range(0, len(all_inputs[a])):
            for c in range(0, len(all_inputs[a][b])):
                latin_word = strip_accents(all_inputs[a][b][c])

                driver.execute_script("arguments[0].scrollIntoView();", latin_inputs[a])

                latin_inputs[a].clear()
                latin_inputs[a].send_keys(latin_word)
                latin_inputs[a].send_keys(Keys.ENTER + ' a')

                while len(str(latin_inputs[i].text).split('\n')) != 1:
                    time.sleep(.1)

                time.sleep(.25)

                default_color = 'green'
                if 'color:red' in str(latin_inputs[a].get_attribute('style')).replace(' ', ''):
                    default_color = 'red'

                temp_answers = []
                temp_answers.extend(all_answers[a])
                span_texts = latin_inputs[a].find_elements(By.TAG_NAME, 'span')

                if default_color == 'red' and len(span_texts) != 0 and latin_word not in temp_answers:
                    temp_answers.append(latin_word)
                    print('correct')

                elif default_color == 'green' and len(span_texts) == 0 and latin_word not in temp_answers:
                    temp_answers.append(latin_word)
                    print('correct')

                all_answers[a] = temp_answers

    print(all_answers)
    for a in range(0, len(all_answers)):
        (latin_inputs[a]).clear()
        time.sleep(.5)

        driver.execute_script("arguments[0].scrollIntoView();", latin_inputs[a])

        for b in range(0, len(all_answers[a])):
            latin_inputs[a].send_keys(all_answers[a][b])

            if b != len(all_answers[a]) - 1:
                latin_inputs[a].send_keys(' ')
        
        latin_inputs[a].send_keys(Keys.ENTER)