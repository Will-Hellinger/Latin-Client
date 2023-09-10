from web_driver import *
import json
import time
from info import *

dictionary = 'latin_dictionary'
keys_dictionary = 'reading_keys'


def scan_for_word(list: list, word: str) -> bool:
    """
    Check if a given word exists in a list of tuples.

    :param list: The list of tuples to search.
    :param word: The word to search for.
    :return: True if the word is found, otherwise False.
    """

    for a in range(len(list)):
        if list[a][1] == word:
            return True
    return False


def scan_words() -> list:
    """
    Scan for Latin words on a web page and return a list of web elements.

    :return: A list of web elements containing Latin words.
    """

    latin_word_elements = driver.find_elements(By.XPATH, '// span[@class="tappit latin"]')
    latin_word_texts = []
    temp_latin_words = []

    for a in range(len(latin_word_elements)):
        latin_word_texts.append([a, str(latin_word_elements[a].text)])
    
    for a in range(len(latin_word_texts)):
        file_name = encode_file_name(latin_word_texts[a][1])

        if not os.path.exists(f'.{subDirectory}data{subDirectory}{dictionary}{subDirectory}{file_name}.json'):
            temp_latin_words.append(latin_word_texts[a])
        else:
            with open(f'.{subDirectory}data{subDirectory}{dictionary}{subDirectory}{file_name}.json', mode='r+') as file:
                wordData = json.load(file)
            if len(wordData) == 0:
                temp_latin_words.append(latin_word_texts[a])
    
    latin_word_texts = []
    for a in range(len(temp_latin_words)):
        if not scan_for_word(latin_word_texts, temp_latin_words[a]):
            latin_word_texts.append(temp_latin_words[a])
    
    temp_latin_words = []
    for a in range(len(latin_word_texts)):
        temp_latin_words.append(latin_word_elements[latin_word_texts[a][0]])

    return temp_latin_words


def learn_words() -> None:
    """
    Learn Latin words from a web page, save definitions, and manage data.

    :return: None
    """

    print('Prepping Elements...', end='\r')
    latin_words = scan_words()

    for a in range(len(latin_words)):
        print(f'Scanning: {round((100/len(latin_words))*(a+1))}%        ', end='\r')

        driver.execute_script("arguments[0].scrollIntoView();", latin_words[a])
        file_name = encode_file_name(latin_words[a].text)

        if not os.path.exists(f'.{subDirectory}data{subDirectory}{dictionary}{subDirectory}{file_name}.json'):
            with open(f'.{subDirectory}data{subDirectory}{dictionary}{subDirectory}{file_name}.json', mode='w') as file:
                file.write('{\n}')

        with open(f'.{subDirectory}data{subDirectory}{dictionary}{subDirectory}{file_name}.json', mode='r+') as file:
            data = json.load(file)

            latin_words[a].click()
            time.sleep(.5)
            parent_element = driver.find_elements(By.TAG_NAME, 'ol')

            if len(parent_element) == 2:
                definitions = parent_element[1].find_elements(By.TAG_NAME, "li")
                for b in range(len(definitions)):
                    data[definitions[b].text] = True
            elif len(parent_element) == 1:
                definition = driver.find_elements(By.TAG_NAME, 'em')
                definition = definition[len(definition)-1].text
                data[definition] = True
            save_file(file, data)

    print('Done Scanning        ')


def build_key() -> None:
    """
    Build a key for a reading exercise and save it to a JSON file.

    :return: None
    """
    
    global keys_dictionary

    user = str(str(str(driver.find_element(By.ID, 'graspHead').text).split("'s")[0]).upper())
    reading_name = str(driver.find_element(By.ID, 'graspHead').text).replace(f"{user}'s ", '')
    
    print(f'Building key for: {reading_name}')

    reading_name = encode_file_name(reading_name)

    if not os.path.exists(f'.{subDirectory}data{subDirectory}{keys_dictionary}{subDirectory}{reading_name}.json'):
        with open(f'.{subDirectory}data{subDirectory}{keys_dictionary}{subDirectory}{reading_name}.json', mode='w') as file:
            file.write('{\n"percentage" : "0%",\n"answers" : {}}')

    with open(f'.{subDirectory}data{subDirectory}{keys_dictionary}{subDirectory}{reading_name}.json', encoding='utf-8', mode='r+') as file:
        data = json.load(file)
        grasp_length = driver.execute_script('var denom = $("[data-grasp]").length; return denom;')

        data['percentage'] = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text).replace(' correct', '')

        if data.get('answers') is None:
            data['answers'] = {}
        
        for a in range(grasp_length):
            textbox = driver.find_element(By.XPATH, f'// textarea[@data-grasp="{a+1}"]')
            driver.execute_script("arguments[0].scrollIntoView();", textbox)

            if 'rgb(0, 128, 0)' in str(textbox.get_attribute('style')): #rgb(0, 128, 0) is the correct color indicator (green)
                if data['answers'].get(a+1) is None:
                    data['answers'][a+1] = str(textbox.text)
        save_file(file, data)