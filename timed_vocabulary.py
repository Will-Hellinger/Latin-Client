from web_driver import *
import time, json
from info import *


try:
    from googletrans import Translator
    translator = Translator()
    #test to see if translator works and fast enough first
    translater_delay = time.time()
    translator.translate('le tit', src='fr', dest='en')
    translater_delay = time.time() - translater_delay

    if translater_delay < 2: #disabled for now cause im lazy
        runPrediction = True
        import nltk
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        from nltk.corpus import wordnet
    else:
        runPrediction = False
        print('prediction mode disabled')
    
except:
    runPrediction = False
    print('prediction mode disabled')

vocab_element = 'timedVocab_lemma'
definition_element = 'timedVocab_def'
false_element = 'timed_vocab_answer_false'
true_element = 'timed_vocab_answer_true'
timer_element = 'timed_vocab_timer'
vocab_dictionary = 'timed_vocabulary_dictionary'


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
    
    response = str(ui_title.text).split('\n')[1]
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
        if word1 == str(driver.find_element(By.ID, vocab_element).text).split('\n')[0] and word2 == str(driver.find_element(By.ID, definition_element).text):
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

    word = str(driver.find_element(By.XPATH, f"// p[@id='{vocab_element}']").text).split('\n')[0]
    definition = str(driver.find_element(By.XPATH, f"// p[@id='{definition_element}']").text)
    predicted_guess = "none"

    #This is honestly only for windows
    file_name = encode_file_name(str(word))

    if not os.path.exists(f'.{subDirectory}data{subDirectory}{vocab_dictionary}{subDirectory}{file_name}.json'):
        print(f'{word} not found, creating entry.', end='\r')
        with open(f'.{subDirectory}data{subDirectory}{vocab_dictionary}{subDirectory}{file_name}.json', 'w') as temp_file:
            temp_file.write('{\n}')
    
    with open(f'.{subDirectory}data{subDirectory}{vocab_dictionary}{subDirectory}{file_name}.json', encoding='utf-8', mode='r+') as file:
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
                save_file(file, data)
            elif check_true() == None:
                print('Inactivity or invalid security label')
                
        elif definition not in items:
            print(f'no entry for {definition} within {word}', end='\r')

            if runPrediction == True:
                translated_word = (translator.translate(word, src='la', dest='en').text)
                translated_word_synonyms = synonym_extractor(translated_word)
                #just to make sure it's added
                translated_word_synonyms.append(translated_word)
                translated_word_antonyms = antonym_extractor(translated_word)

                data_antonyms = []
                data_synonyms = []
                for item in data:
                    if data[item] == False:
                        data_antonyms = antonym_extractor(item)
                        data_antonyms.append(item)
                    elif data[item] == True:
                        data_synonyms = synonym_extractor(item)
                        data_synonyms.append(item)
                    
                if definition in translated_word_synonyms or definition in data_synonyms:
                    predicted_guess = True
                elif definition in translated_word_antonyms or definition in data_antonyms:
                    predicted_guess = False
            
            if predicted_guess == True:
                driver.find_element(By.XPATH, f"// label[@for='{true_element}']").click()
            else:
                driver.find_element(By.XPATH, f"// label[@for='{false_element}']").click()

            wait_reload(word, definition)
            if check_true() == True and predicted_guess != "none":
                data[definition] = predicted_guess
                print(f'Predicted Guess - {predicted_guess}: {word} - {definition}: Correct')
            elif check_true() == True and predicted_guess == "none":
                data[definition] = False
                print(f'Guess - False: {word} - {definition}: Correct')
            elif check_true() == False and predicted_guess != "none":
                data[definition] = not predicted_guess
                print(f'Predicted Guess - {predicted_guess}: {word} - {definition}: Incorrect')
            elif check_true() == False and predicted_guess == "none":
                data[definition] = True
                print(f'Guess - False: {word} - {definition}: Inorrect')
            elif check_true() == None:
                print('Inactivity or invalid security label')
            save_file(file, data)
    
    human_timeout(1000, 2000)