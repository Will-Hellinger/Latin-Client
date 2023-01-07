from web_driver import *
import time, json, random

def spam_true():
    driver.find_element(By.XPATH, f"// label[@for='timed_morphology_answer_true']").click()
    time.sleep(.5)

def spam_false():
    driver.find_element(By.XPATH, f"// label[@for='timed_morphology_answer_false']").click()
    time.sleep(.5)

def solver():
    word1 = str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_form']").text)
    word2 = str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_stimulus']").text)
    print(word1, word2)
    read_file = open("timed_dictionary.json", encoding='utf-8').read()
    with open("timed_dictionary.json", encoding='utf-8', mode='r+') as file:
        data = json.load(file)
        if (str((word1.encode('unicode-escape')).decode('utf-8') + ' - ' + (word2.encode('unicode-escape')).decode('utf-8'))) in read_file:
            try:
                print(data[(word1 + ' - ' + word2)])
                if data[(word1 + ' - ' + word2)] == True:
                    driver.find_element(By.XPATH, f"// label[@for='timed_morphology_answer_true']").click()
                else:
                    driver.find_element(By.XPATH, f"// label[@for='timed_morphology_answer_false']").click()
                while True:
                    if str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_form']").text) == word1 and str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_stimulus']").text) == word2:
                        time.sleep(.5)
                    else:
                        break
                if ((str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).endswith((str(int(str(driver.find_element(By.XPATH, f"// p[@id='laststreak']").text).split(': ')[1]) + 1) + '.')) and 'current streak is' in (str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).lower()) or 'freak' in (str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).lower():
                    print(f'Found in dictionary: {word1} - {word2}: Correct')
                else:
                    print(f'Found in dictionary: {word1} - {word2}: Incorrect, switching now...')
                    data[(word1 + ' - ' + word2)] = not data[(word1 + ' - ' + word2)]
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()

            except:
                print('unable to load... Attempting to "relearn"')
                driver.find_element(By.XPATH, f"// label[@for='timed_morphology_answer_false']").click()
                while True:
                    if str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_form']").text) == word1 and str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_stimulus']").text) == word2:
                        time.sleep(.5)
                    else:
                        break
                if ((str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).endswith((str(int(str(driver.find_element(By.XPATH, f"// p[@id='laststreak']").text).split(': ')[1]) + 1) + '.')) and 'current streak is' in (str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).lower()) or 'freak' in (str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).lower():
                    data[word1 + ' - ' + word2] = False
                    print(f'Guess - False: {word1} - {word2}: Correct')
                else:
                    data[word1 + ' - ' + word2] = True
                    print(f'Guess - False: {word1} - {word2}: Incorrect')
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
        else:
            driver.find_element(By.XPATH, f"// label[@for='timed_morphology_answer_false']").click()
            while True:
                if str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_form']").text) == word1 and str(driver.find_element(By.XPATH, f"// p[@id='timedMorph_stimulus']").text) == word2:
                    time.sleep(.5)
                else:
                    break
            if ((str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).endswith((str(int(str(driver.find_element(By.XPATH, f"// p[@id='laststreak']").text).split(': ')[1]) + 1) + '.')) and 'current streak is' in (str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).lower()) or 'freak' in (str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']").text).split('\n')[0]).lower():
                data[word1 + ' - ' + word2] = False
                print(f'Guess - False: {word1} - {word2}: Correct')
            else:
                data[word1 + ' - ' + word2] = True
                print(f'Guess - False: {word1} - {word2}: Incorrect')
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()