from web_driver import *
import time, json, random
from info import *
try:
    from googletrans import Translator
    translator = Translator()
    #test to see if translator works first
    translator.translate('le tit', src='fr', dest='en')
    import nltk
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    from nltk.corpus import wordnet
    runPrediction = True
except:
    runPrediction = False

vocab_element = 'timedVocab_lemma'
definition_element = 'timedVocab_def'
false_element = 'timed_vocab_answer_false'
true_element = 'timed_vocab_answer_true'

def check_true():
    if 'freak' in str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).lower():
        return True
    response = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[1]
    score = int(str(driver.find_element(By.XPATH, f"// p[@id='laststreak']").text).split(': ')[1])
    if (response.endswith((str(score + 1) + '.')) and 'current streak is' in response.lower()):
        return True
    else:
        return False

def wait_reload(word1: str, word2: str):
    while True:
        if word1 == str(driver.find_element(By.XPATH, f"// p[@id='{vocab_element}']").text).split('\n')[0] and word2 == str(driver.find_element(By.XPATH, f"// p[@id='{definition_element}']").text):
            time.sleep(.5)
        else:
            break

def synonym_extractor(phrase):
    synonyms = []
    for syn in wordnet.synsets(phrase):
        for l in syn.lemmas():
            synonyms.append(l.name())

    return synonyms

def antonym_extractor(phrase):
    antonyms = []
    
    for syn in wordnet.synsets(phrase):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    
    return antonyms

def save_file(file: bytes, data: dict):
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()

def solver():
    word = str(driver.find_element(By.XPATH, f"// p[@id='{vocab_element}']").text).split('\n')[0]
    definition = str(driver.find_element(By.XPATH, f"// p[@id='{definition_element}']").text)
    file_name = (str(word.replace(" ", "_")).encode("unicode-escape")).decode("utf-8").replace("\\", "^")
    #This is honestly only for windows
    removeList = ['\\', '?', '%', '*', ':', '|', '"', '<', '>']
    replaceList = ['(bs)', '(qm)', '(ps)', '(a)', '(c)', '(p)', '(qm)', '(fa)', '(ba)']
    for a in range(len(removeList)):
        file_name = file_name.replace(str(removeList[a]), str(replaceList[a]))
    predicted_guess = "none"

    if runPrediction == True:
        translated_word = (translator.translate(word, src='la', dest='en').text)
        translated_word_synonyms = synonym_extractor(translated_word)
        #just to make sure it's added
        translated_word_synonyms.append(translated_word)
        translated_word_antonyms = antonym_extractor(translated_word)

    if os.path.exists(f'.{subDirectory}data{subDirectory}timed_vocabulary_dictionary{subDirectory}{file_name}.json') == False:
        print(f'word {word} not found, creating entry.')
        with open(f'.{subDirectory}data{subDirectory}timed_vocabulary_dictionary{subDirectory}{file_name}.json', 'w') as temp_file:
            temp_file.write('{\n}')

        with open(f'.{subDirectory}data{subDirectory}timed_vocabulary_dictionary{subDirectory}{file_name}.json', encoding='utf-8', mode='r+') as file:
            data = json.load(file)
            if runPrediction == True:
                if definition in translated_word_synonyms:
                    predicted_guess = True
                elif definition in translated_word_antonyms:
                    predicted_guess = False
            
            if predicted_guess == True:
                driver.find_element(By.XPATH, f"// label[@for='{true_element}']").click()
            else:
                driver.find_element(By.XPATH, f"// label[@for='{false_element}']").click()

            wait_reload(word, definition)
            if check_true():
                if predicted_guess != "none":
                    data[definition] = predicted_guess
                    print(f'Predicted Guess - {predicted_guess}: {word} - {definition}: Correct')
                else:
                    data[definition] = False
                    print(f'Guess - False: {word} - {definition}: Correct')
            else:
                if predicted_guess != "none":
                    data[definition] = not predicted_guess
                    print(f'Predicted Guess - {predicted_guess}: {word} - {definition}: Incorrect')
                else:
                    data[definition] = True
                    print(f'Guess - False: {word} - {definition}: Incorrect')
            save_file(file, data)
    else:
        with open(f'.{subDirectory}data{subDirectory}timed_vocabulary_dictionary{subDirectory}{file_name}.json', encoding='utf-8', mode='r+') as file:
            data = json.load(file)
            items = []
            for item in data:
                items.append(item)
            if definition in items:
                if data[definition] == True:
                    driver.find_element(By.XPATH, f"// label[@for='{true_element}']").click()
                else:
                    driver.find_element(By.XPATH, f"// label[@for='{false_element}']").click()
                wait_reload(word, definition)
                if check_true():
                    print(f'Found in dictionary: {word} - {definition} - {data[definition]}: Correct')
                else:
                    if word in str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text) and definition in str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text):
                        if 'not' in str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text):
                            if data[definition] == False:
                                print(f'Assuming timeout on word {word}')
                            elif data[definition] == True:
                                print(f'Found in dictionary: {word} - {definition} - {data[definition]}: Incorrect, switching now...')
                                data[definition] = not data[definition]
                                save_file(file, data)
                        else:
                            if data[definition] == False:
                                print(f'Found in dictionary: {word} - {definition} - {data[definition]}: Incorrect, switching now...')
                                data[definition] = not data[definition]
                                save_file(file, data)
                            elif data[definition] == True:
                                print(f'Assuming timeout on word {word}')
                    else:
                        print(f'Assuming timeout on word {word}')
            else:
                print(f'no entry within word {word} for {definition}, creating one now.')
                for item in data:
                    if data[item] == False:
                        data_antonyms = antonym_extractor(item)
                    else:
                        data_synonyms = synonym_extractor(item)

                if runPrediction == True:
                    if definition in translated_word_synonyms:
                        predicted_guess = True
                    elif definition in translated_word_antonyms:
                        predicted_guess = False
                try:
                    if definition in data_synonyms:
                        predicted_guess = True
                    elif definition in data_antonyms:
                        predicted_guess = False
                except:
                    pass

                if predicted_guess == True:
                    driver.find_element(By.XPATH, f"// label[@for='{true_element}']").click()
                else:
                    driver.find_element(By.XPATH, f"// label[@for='{false_element}']").click()

                wait_reload(word, definition)
                if check_true():
                    if predicted_guess != "none":
                        data[definition] = predicted_guess
                        print(f'Predicted Guess - {predicted_guess}: {word} - {definition}: Correct')
                    else:
                        data[definition] = False
                        print(f'Guess - False: {word} - {definition}: Correct')
                else:
                    if predicted_guess != "none":
                        data[definition] = not predicted_guess
                        print(f'Predicted Guess - {predicted_guess}: {word} - {definition}: Incorrect')
                    else:
                        data[definition] = True
                        print(f'Guess - False: {word} - {definition}: Inorrect')
                save_file(file, data)