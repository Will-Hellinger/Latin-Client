import custom_translator
from web_driver import *
import time
from info import *
from googletrans import Translator


#TODO: Change way of formatting text from the site...
def learn() -> None:
    """
    Learn Latin-English vocabulary from a web page and update a local dictionary.

    This function scrapes Latin and English vocabulary from a web page and updates a local dictionary. It extracts
    Latin words, their corresponding English translations, and morphological information from the web page and stores
    them in JSON files for future reference.

    :return: None
    """

    english_words = []

    parentElement = driver.find_element(By.CLASS_NAME, 'ui-block-a')
    dictBlock = driver.find_element(By.CLASS_NAME, 'ui-block-b')

    dict_input = dictBlock.find_element(By.XPATH, "// input[@data-type='search']")
    listview = dictBlock.find_element(By.XPATH, "// ul[@data-role='listview']")

    english_vocab = listview.find_elements(By.XPATH, "// h4[@style='text-align:left;font-weight:400']")
    latin_vocab = listview.find_elements(By.XPATH, "// p[@class='latin']")

    path = f'.{subDirectory}data{subDirectory}temp_dictionary{subDirectory}'

    for a in range(0, len(english_vocab)):
        term_element = english_vocab[a]
        latin_words = []
        
        latin_words_elements = latin_vocab[a].find_elements(By.TAG_NAME, "span")

        for latin_word_element in latin_words_elements:
            latin_words.append(str(latin_word_element.text))        
        
        if len(latin_words) == 0:
            latin_words = str(latin_vocab[a].text).split(', ')
        
        for b in range(0, len(latin_words)):
            latin_words[b] = latin_words[b].replace(',', '')
            if '(' in latin_words[b]:
                latin_words[b] = latin_words[b].split(' (')[0]

        english_word = ''
        term = str(term_element.text).replace('\n',' ')

        if ')' in term and ':' not in term and term.startswith('('):
            english_word = term.split(') ')[1]
        elif ')' in term and ': ' in term and term.startswith('('):
            english_word = term.split(': ')[1]
            english_word = english_word.split(')')[0]
        elif not term.startswith('(') and ')' in term:
            english_word = term.split(' (')[0]
        elif ')' not in term and 'note:' not in term:
            english_word = term
        elif ')' not in term and 'note:' in term:
            english_word = term.split('\n')[0]
        
        english_word = english_word.replace(':', '')
        english_word = strip_accents(english_word)

        if '...' in english_word:
            english_word = english_word.split('... ')
        elif ',' in english_word:
            english_word = english_word.split(', ')

        print(latin_words)

        for latin_word in latin_words:
            if '-' in latin_word or latin_word == 'f.' or latin_word == 'm.' or latin_word == 'n.':
                pass

            filename = encode_file_name(latin_word)

            if not os.path.exists(f'{path}{filename}.json'):
                with open(f'{path}{filename}.json', mode='w') as file:
                    file.write('{\n}')
            
            with open(f'{path}{filename}.json', mode='r+') as file:
                data = json.load(file)

                if isinstance(english_word, list):
                    for word in english_word:
                        word = word.replace('...', '')
                        word = word.replace(':', '')

                        data[word] = True
                else:
                    english_word = english_word.replace('...', '')
                    english_word = english_word.replace(':', '')

                    data[english_word] = True
                
                save_file(file, data)


def solve() -> None:
    """
    Solve Latin-English composition assignments.

    This function solves Latin-English composition assignments by extracting English text, translating it to Latin, and
    entering the Latin translations into text input fields on a web page. It also handles translation fallback using
    Google Translate if enabled.

    :return: None
    """

    parentElement = driver.find_element(By.CLASS_NAME, 'ui-block-a')
    english_texts = parentElement.find_elements(By.XPATH, "// p[@style='white-space:pre-wrap;margin-right:2em;font-size:1em']")
    latin_inputs = parentElement.find_elements(By.XPATH, "// div[@class='latin composition ui-input-text ui-shadow-inset ui-body-inherit ui-corner-all ui-textinput-autogrow']")
    assignment_header = driver.find_element(By.ID, 'assessHead')
    dictionary = custom_translator.get_dictionary()


    all_inputs = []

    if compositions_fallback == True:
        try:
            translator = Translator()
            translator.translate('le tit', src='fr', dest='en')
            print('google trans enabled')
        except:
            translator = None
            print('google trans disabled')
    else:
        print('google trans disabled')
    
    for a in range(0, len(english_texts)):
        english_texts[a] = (english_texts[a].text).lower().replace(',', '').replace('.', '')

    for english_text in english_texts:
        if compositions_fallback == True and translator is not None:
            trans_words = str(translator.translate(english_text, dest='la', src='en').text)
            trans_words = trans_words.replace('.', '')
            trans_words = trans_words.replace(',', '')

            trans_words = trans_words.split(' ')
            
        english_text = english_text.split(' ')

        processed_words = []

        inputs = []
        for i in range(len(english_text)):
            for j in range(i+1, len(english_text)+1):
                combined_word = ''.join(english_text[i:j])
                synonyms = None

                if compositions_synonyms_enabled == True:
                    synonyms = synonym_extractor(combined_word)

                if combined_word in processed_words:
                    continue
                    
                processed_words.append(combined_word)

                output = []

                if synonyms is not None or synonyms != [] and compositions_synonyms_enabled == True:
                    for synonym in synonyms:
                        processed_words.append(synonym)

                        synonym_translation = custom_translator.translate(word=synonym, language='english', dictionary=dictionary, use_base=False)
                        base_synonym_translation = custom_translator.translate(word=synonym, language='english', dictionary=dictionary, use_base=False)

                        if synonym_translation is not None and synonym_translation not in output:
                            output.extend(synonym_translation)

                        if base_synonym_translation is not None and base_synonym_translation not in output:
                            output.extend(base_synonym_translation)

                translation_output = custom_translator.translate(word=combined_word, language='english', dictionary=dictionary, use_base=False)
                base_translation_output = custom_translator.translate(word=combined_word, language='english', dictionary=dictionary, use_base=True)

                if translation_output is not None and translation_output not in output:
                    output.extend(translation_output)
                
                if base_translation_output is not None and base_translation_output not in output:
                    output.extend(base_translation_output)

                if output is not None:
                    inputs.append(output)
        
        if compositions_fallback == True and translator is not None:
            inputs.append(trans_words)
        
        all_inputs.append(inputs)
    all_answers = []

    assignment_name = str(assignment_header.text)
    user = assignment_name.split("'s ")[0]
    assignment_name = assignment_name.replace(f"{user}'s ", "")
    assignment_name = encode_file_name(assignment_name)

    if not os.path.exists(f'.{subDirectory}data{subDirectory}cache{subDirectory}{assignment_name}.json'):
        with open(f'.{subDirectory}data{subDirectory}cache{subDirectory}{assignment_name}.json', mode='w', encoding='utf-8') as file:
            file.write('{\n}')

    for latin_input in latin_inputs:
        driver.execute_script("arguments[0].scrollIntoView();", latin_input)
        default_color = 'green'
        answers = []

        if 'color:red' in str(latin_input.get_attribute('style')).replace(' ', ''):
            default_color = 'red'
        
        span_texts = latin_input.find_elements(By.TAG_NAME, 'span')
        text = latin_input.text

        if default_color == 'green':
            if len(span_texts) != 0:
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

    cache_file = open(f'.{subDirectory}data{subDirectory}cache{subDirectory}{assignment_name}.json', mode='r+', encoding='utf-8')
    data = json.load(cache_file)

    for english_text in english_texts:
        if data.get(english_text) is not None:
            continue
        
        temp_dicionary = {'correct' : [], 'incorrect' : []}
        data[english_text] = temp_dicionary
    
    save_file(cache_file, data)

    for a in range(0, len(all_inputs)):
        for b in range(0, len(all_inputs[a])):
            for c in range(0, len(all_inputs[a][b])):
                latin_word = strip_accents(all_inputs[a][b][c])

                driver.execute_script("arguments[0].scrollIntoView();", latin_inputs[a])

                if latin_word in data[english_texts[a]]['incorrect']:
                    continue
                
                elif latin_word in data[english_texts[a]]['correct']:
                    if latin_word not in all_answers[a]:
                        all_answers[a].append(latin_word)
                    
                    continue

                latin_inputs[a].clear()
                latin_inputs[a].send_keys(latin_word)
                latin_inputs[a].send_keys(Keys.ENTER + ' a')

                while len(str(latin_inputs[a].text).split('\n')) != 1:
                    time.sleep(.05)

                time.sleep(.05)

                default_color = 'green'
                if 'color:red' in str(latin_inputs[a].get_attribute('style')).replace(' ', ''):
                    default_color = 'red'

                span_texts = latin_inputs[a].find_elements(By.TAG_NAME, 'span')

                if default_color == 'red' and len(span_texts) != 0 and latin_word not in all_answers[a]:
                    all_answers[a].append(latin_word)

                elif default_color == 'green' and len(span_texts) == 0 and latin_word not in all_answers[a]:
                    all_answers[a].append(latin_word)
                
                else:
                    temp_list = data[english_texts[a]]['incorrect']
                    temp_list.append(latin_word)
                    data[english_texts[a]]['incorrect'] = temp_list

                human_timeout(1000, 5000)

        data[english_texts[a]]['correct'] = all_answers[a]
        save_file(cache_file, data)

        (latin_inputs[a]).clear()
        time.sleep(.5)

        used_words = [] #backup repitition check
        driver.execute_script("arguments[0].scrollIntoView();", latin_inputs[a])

        for b in range(0, len(all_answers[a])):
            if all_answers[a][b] in used_words:
                continue
            
            latin_inputs[a].send_keys(all_answers[a][b])
            if b != len(all_answers[a]) - 1:
                latin_inputs[a].send_keys(' ')
            
            used_words.append(all_answers[a][b])

        latin_inputs[a].send_keys(Keys.ENTER)

    cache_file.close()