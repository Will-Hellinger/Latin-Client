from web_driver import *
from info import *
import time
import json
import os



noun_adj_chart = f'.{subDirectory}data{subDirectory}noun-adj_chart.json'


def check_dictionary(words: list) -> bool:
    """
    Check if words are present in the dictionary and return a response.

    :param words: A list of words to check.
    :return: A response (True or False) if words are found in the dictionary, otherwise None.
    """

    for word in range(0, len(words)):
        file_path = f'.{subDirectory}data{subDirectory}noun_adjective_dictionary{subDirectory}{encode_file_name(words[word])}.json'

        if os.path.exists(file_path):
            dictionary_data = json.load(open(file_path, mode='r', encoding='utf-8'))
            
            if word == 0 and dictionary_data.get(encode_file_name(words[1])) is not None:
                return dictionary_data.get(encode_file_name(words[1]))

            elif word == 1 and dictionary_data.get(encode_file_name(words[0])) is not None:
                return dictionary_data.get(encode_file_name(words[0]))
    
    return None


def prediction(words: list = None) -> bool:
    """
    Predict if a given list of words forms a valid combination based on available endings.

    :param words: A list of words to predict.
    :return: True if a valid combination is predicted, otherwise False.
    """

    if len(words) != 2 or words is None:
        return False
    

    data = json.load(open(noun_adj_chart, mode='r', encoding='utf-8'))
    endings = []

    for word in words:
        all_endings = []

        for end in data:
            if word.endswith(end):
                all_endings.append(end)

        if len(all_endings) >= 1:
            endings.append(max(all_endings, key=len))
    
    for ending in data[endings[0]]:
        if ending in data[endings[1]]:
            return True
    
    return False


def solver() -> None:
    """
    Perform a series of actions, including solving word combinations and managing responses.

    :return: None
    """
    
    dictionary_inputs = 0
    nouns = []
    responses = []

    for a in range(10):
        if loadWait(By.NAME, f'input{str(a+1)}'):
            nouns.append((driver.find_element(By.NAME, f'input{str(a+1)}').text).split('\n')[0])
    
    for a in range(len(nouns)):
        if 'noun' not in str(driver.title).lower():
            break

        try:
            if a != 0:
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, f'// label[@for="no{a}"]'))
            else:
                driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.HOME)
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, f'// label[@for="no1"]'))
        except:
            print(f'unable to scroll to element {a}')


        if 'noun' not in str(driver.title).lower():
            break

        words = nouns[a].split(' ')

        if check_dictionary(words) is None:
            output = prediction(words)
            responses.append({"word1" : words[0], "word2" : words[1], "prediction based" : True, "response" : output})
        else:
            output = check_dictionary(words)
            responses.append({"word1" : words[0], "word2" : words[1], "prediction based" : False, "response" : output})
            dictionary_inputs += 1

        choice = 'no'
        if output == True:
            choice = 'yes'
        
        try:
            if loadWait(By.XPATH, f'// label[@for="{choice}{a+1}"]'):
                driver.find_element(By.XPATH, f'// label[@for="{choice}{a+1}"]').click()
        except:
            print(f'unable to press {choice}{a+1}')

        human_timeout(1000, 5000)

    selections = ['agreeSubmit', 'agreeMore']

    for selection in selections:
        while True:
            if 'noun' not in str(driver.title).lower():
                break

            try:
                if not loadWait(By.ID, selection):
                    break
                    
                driver.find_element(By.ID, selection).click()
                break
            except:
                print(f'unable to press get {selection}')
                time.sleep(2)

    time.sleep(5)

    response_text = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text).split('\n')[0]
    correct_amount = str(response_text.split(' out of ')[0])
    correct_amount = int(correct_amount.replace('You answered ', ''))

    if correct_amount == 10 and dictionary_inputs != 10:
        for response in responses:

            if response['prediction based'] == True and check_dictionary([response['word1'], response['word2']]) is None:
                response_path = f'.{subDirectory}data{subDirectory}noun_adjective_dictionary{subDirectory}{encode_file_name(response["word1"])}.json'

                with open(response_path, mode='w', encoding='utf-8') as file:
                    file.write('{\n}')
                
                with open(response_path, mode='r+', encoding='utf-8') as file:
                    response_data = json.load(file)
                    response_data[encode_file_name(response['word2'])] = response['response']
                    save_file(file, response_data)

    if correct_amount == dictionary_inputs:
        for response in responses:

            if response['prediction based'] == True and check_dictionary([response['word1'], response['word2']]) is None:
                response_path = f'.{subDirectory}data{subDirectory}noun_adjective_dictionary{subDirectory}{encode_file_name(response["word1"])}.json'

                with open(response_path, mode='w', encoding='utf-8') as file:
                    file.write('{\n}')
                
                with open(response_path, mode='r+', encoding='utf-8') as file:
                    response_data = json.load(file)
                    response_data[encode_file_name(response['word2'])] = not response['response']
                    save_file(file, response_data)

    try:
        print(f'{response_text} | Dictionary Inputs: {dictionary_inputs} | Predictions: {10 - dictionary_inputs}')
    except:
        print('unable to get score')