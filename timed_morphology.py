from web_driver import *
import time
import json
from info import *

form_element = 'timedMorph_form'
stimuli_element = 'timedMorph_stimulus'
false_element = 'timed_morphology_answer_false'
true_element = 'timed_morphology_answer_true'
timer_element = 'timed_morphology_timer'
morphology_dictionary = 'timed_morphology_dictionary'

def check_true() -> bool:
    """
    Check if the current question is marked as true (correct).

    :return: True if the question is marked as true, False if marked as false, or None if the question has expired or
             has an invalid security label.
    """

    ui_title = driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']")
    if 'freak' in str(ui_title.text).lower():
        return True
    if 'This question has expired due to inactivity or it has an invalid security label.' == str(ui_title.text):
        return None
    response = str(ui_title.text).split('\n')[0]
    score = int(str(driver.find_element(By.XPATH, f"// p[@id='laststreak']").text).split(': ')[1])
    if (response.endswith((str(score + 1) + '.')) and 'current streak is' in response.lower()):
        return True
    else:
        return False

def check_timout(word: str, definition: str, data: dict) -> bool:
    """
    Check if a question has timed out or if its definition matches the expected one.

    :param word: The word associated with the question.
    :param definition: The expected definition of the word.
    :param data: A dictionary containing definitions and their correctness status.
    :return: True if the question has timed out or if its definition does not match the expected one, False otherwise.
    """

    ui_title = driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']")

    if word in str(ui_title.text) and definition in str(ui_title.text):
        if 'not' in str(ui_title.text) and data[definition] == False:
            return True
        elif 'not' not in str(ui_title.text) and data[definition] == True:
            return True
        else:
            return False
    else:
        return True


def wait_reload(word1: str, word2: str) -> None:
    """
    Wait for the page to reload with new words.

    :param word1: The first word to wait for.
    :param word2: The second word to wait for.
    :return: None
    """

    while True:
        if word1 == str(driver.find_element(By.XPATH, f"// p[@id='{form_element}']").text).split('\n')[0] and word2 == str(driver.find_element(By.XPATH, f"// p[@id='{stimuli_element}']").text):
            time.sleep(.5)
        else:
            time.sleep(1)
            break


def solver() -> None:
    """
    Automatically solve timed morphology questions on a web page.

    This function automates the process of answering timed morphology questions on a web page. It retrieves information
    about the current question, checks if it's already present in the dictionary, and submits an answer accordingly.

    :return: None
    """
    
    word = str(driver.find_element(By.XPATH, f"// p[@id='{form_element}']").text).split('\n')[0]
    definition = str(driver.find_element(By.XPATH, f"// p[@id='{stimuli_element}']").text)

    #This is honestly only for windows
    file_name = encode_file_name(str(word))

    if not os.path.exists(f'.{subDirectory}data{subDirectory}{morphology_dictionary}{subDirectory}{file_name}.json'):
        print(f'{word} not found, creating entry.', end='\r')
        with open(f'.{subDirectory}data{subDirectory}{morphology_dictionary}{subDirectory}{file_name}.json', 'w') as temp_file:
            temp_file.write('{\n}')
    
    with open(f'.{subDirectory}data{subDirectory}{morphology_dictionary}{subDirectory}{file_name}.json', encoding='utf-8', mode='r+') as file:
        data = json.load(file)
        items = list(data.keys())

        if definition in items:
            print('Found in dictionary: ...', end='\r')

            if data[definition] == True:
                driver.find_element(By.XPATH, f"// label[@for='{true_element}']").click()
            elif data[definition] == False:
                driver.find_element(By.XPATH, f"// label[@for='{false_element}']").click()
            wait_reload(word, definition)

            if check_true() == True:
                print(f'Found in dictionary: {word} - {definition} - {data[definition]}: Correct')
            elif check_true() == False and check_timout(word, definition, data) == True:
                print(f'Assuming timeout on word {word}')
            elif check_true() == False and check_timout(word, definition, data) == False:
                print(f'Found in dictionary: {word} - {definition} - {data[definition]}: Incorrect, switching now...')
                data[definition] = not data[definition]
            elif check_true() == None:
                print('Inactivity or invalid security label')


        elif definition not in items:
            print(f'no entry for {definition} within {word}', end='\r')
            driver.find_element(By.XPATH, f"// label[@for='{false_element}']").click()

            wait_reload(word, definition)
            if check_true() == True:
                data[definition] = False
                print(f'Guess - False: {word} - {definition}: Correct')
            elif check_true() == False:
                data[definition] = True
                print(f'Guess - False: {word} - {definition}: Inorrect')
        
        save_file(file, data)
    
    human_timeout(1000, 2000)