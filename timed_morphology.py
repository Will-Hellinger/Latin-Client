from web_driver import *
import time, json, random
from info import *

def check_true():
    if ((str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).endswith((str(int(str(driver.find_element(By.XPATH, f"// p[@id='laststreak']").text).split(': ')[1]) + 1) + '.')) and 'current streak is' in (str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).lower()) or 'freak' in (str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).lower():
        return True
    else:
        return False

def wait_reload(word1, word2):
    while True:
        if str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_form']").text) == word1 and str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_stimulus']").text) == word2:
            time.sleep(.5)
        else:
            break

def save_file(file, data):
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()

def solver():
    word1 = str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_form']").text)
    word2 = str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_stimulus']").text)

    file_name = (str(word1.replace(" ", "_")).encode("unicode-escape")).decode("utf-8").replace("\\", "^")
    #This is honestly only for windows
    removeList = ['\\', '?', '%', '*', ':', '|', '"', '<', '>']
    replaceList = ['(bs)', '(qm)', '(ps)', '(a)', '(c)', '(p)', '(qm)', '(fa)', '(ba)']
    for a in range(len(removeList)):
        file_name = file_name.replace(str(removeList[a]), str(replaceList[a]))
    
    if os.path.exists(f'.{subDirectory}data{subDirectory}timed_morphology_dictionary{subDirectory}{file_name}.json') == False:
        print(f'word {word1} not found, creating entry.')
        with open(f'.{subDirectory}data{subDirectory}timed_morphology_dictionary{subDirectory}{file_name}.json', 'w') as temp_file:
            temp_file.write('{\n}')
        
        with open(f'.{subDirectory}data{subDirectory}timed_morphology_dictionary{subDirectory}{file_name}.json', encoding='utf-8', mode='r+') as file:
            data = json.load(file)
            driver.find_element(By.XPATH, f"// label[@for='timed_morphology_answer_false']").click()
            while True:
                if str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_form']").text) == word1 and str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_stimulus']").text) == word2:
                    time.sleep(.5)
                else:
                    break
            if check_true():
                data[word2] = False
                print(f'Guess - False: {word1} - {word2}: Correct')
            else:
                data[word2] = True
                print(f'Guess - False: {word1} - {word2}: Incorrect')
            save_file(file, data)
    else:
        with open(f'.{subDirectory}data{subDirectory}timed_morphology_dictionary{subDirectory}{file_name}.json', encoding='utf-8', mode='r+') as file:
            data = json.load(file)
            items = []
            for item in data:
                items.append(item)
            if word2 in items:
                if data[word2] == True:
                    driver.find_element(By.XPATH, f"// label[@for='timed_morphology_answer_true']").click()
                else:
                    driver.find_element(By.XPATH, f"// label[@for='timed_morphology_answer_false']").click()
                while True:
                    if str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_form']").text) == word1 and str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_stimulus']").text) == word2:
                        time.sleep(.5)
                    else:
                        break
                if check_true():
                    print(f'Found in dictionary: {word1} - {word2} - {data[word2]}: Correct')
                else:
                    if word1 in str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text) and word2 in str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text):
                        if 'not' in str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text):
                            if data[word2] == False:
                                print(f'Assuming timeout on word {word1}')
                            elif data[word2] == True:
                                print(f'Found in dictionary: {word1} - {word2} - {data[word2]}: Incorrect, switching now...')
                                data[word2] = not data[word2]
                                save_file(file, data)
                        else:
                            if data[word2] == False:
                                print(f'Found in dictionary: {word1} - {word2} - {data[word2]}: Incorrect, switching now...')
                                data[word2] = not data[word2]
                                save_file(file, data)
                            elif data[word2] == True:
                                print(f'Assuming timeout on word {word1}')
                    else:
                        print(f'Assuming timeout on word {word1}')
            else:
                print(f'no entry within word {word1} for {word2}, creating one now.')
                driver.find_element(By.XPATH, f"// label[@for='timed_morphology_answer_false']").click()
                while True:
                    if str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_form']").text) == word1 and str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_stimulus']").text) == word2:
                        time.sleep(.5)
                    else:
                        break
                if check_true():
                    data[word2] = False
                    print(f'Guess - False: {word1} - {word2}: Correct')
                else:
                    data[word2] = True
                    print(f'Guess - False: {word1} - {word2}: Incorrect')
                save_file(file, data)