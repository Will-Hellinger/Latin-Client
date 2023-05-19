from web_driver import *
import json
import time
from info import *

dictionary = 'latin_dictionary'
keysDictionary = 'reading_keys'


def scanforWord(list: list, word: str):
    for a in range(len(list)):
        if list[a][1] == word:
            return True
    return False


def scan_words():
    latinWordElements = driver.find_elements(By.XPATH, '// span[@class="tappit latin"]')
    latinWordTexts = []
    tempLatinWords = []

    for a in range(len(latinWordElements)):
        latinWordTexts.append([a, str(latinWordElements[a].text)])
    
    for a in range(len(latinWordTexts)):
        file_name = encodeFilename(latinWordTexts[a][1])

        if not os.path.exists(f'.{subDirectory}data{subDirectory}{dictionary}{subDirectory}{file_name}.json'):
            tempLatinWords.append(latinWordTexts[a])
        else:
            with open(f'.{subDirectory}data{subDirectory}{dictionary}{subDirectory}{file_name}.json', mode='r+') as file:
                wordData = json.load(file)
            if len(wordData) == 0:
                tempLatinWords.append(latinWordTexts[a])
    
    latinWordTexts = []
    for a in range(len(tempLatinWords)):
        if not scanforWord(latinWordTexts, tempLatinWords[a]):
            latinWordTexts.append(tempLatinWords[a])
    
    tempLatinWords = []
    for a in range(len(latinWordTexts)):
        tempLatinWords.append(latinWordElements[latinWordTexts[a][0]])
    latinWordElements = tempLatinWords

    return latinWordElements


def learn_words():
    print('Prepping Elements...', end='\r')
    latinWords = scan_words()
    latinWordsLength = len(latinWords)

    for a in range(len(latinWords)):
        print(f'Scanning: {round((100/latinWordsLength)*(a+1))}%        ', end='\r')

        driver.execute_script("arguments[0].scrollIntoView();", latinWords[a])
        file_name = encodeFilename(latinWords[a].text)

        if not os.path.exists(f'.{subDirectory}data{subDirectory}{dictionary}{subDirectory}{file_name}.json'):
            with open(f'.{subDirectory}data{subDirectory}{dictionary}{subDirectory}{file_name}.json', mode='w') as file:
                file.write('{\n}')

        with open(f'.{subDirectory}data{subDirectory}{dictionary}{subDirectory}{file_name}.json', mode='r+') as file:
            data = json.load(file)

            latinWords[a].click()
            time.sleep(.5)
            parentElement = driver.find_elements(By.TAG_NAME, 'ol')

            if len(parentElement) == 2:
                definitions = parentElement[1].find_elements(By.TAG_NAME, "li")
                for b in range(len(definitions)):
                    data[definitions[b].text] = True
            elif len(parentElement) == 1:
                definition = driver.find_elements(By.TAG_NAME, 'em')
                definition = definition[len(definition)-1].text
                data[definition] = True
            save_file(file, data)

    print('Done Scanning        ')


def build_key():
    global keysDictionary

    user = str(str(str(driver.find_element(By.ID, 'graspHead').text).split("'s")[0]).upper())
    readingName = str(driver.find_element(By.ID, 'graspHead').text).replace(f"{user}'s ", '')
    print(f'Building key for: {readingName}')
    readingName = encodeFilename(readingName)

    if not os.path.exists(f'.{subDirectory}data{subDirectory}{keysDictionary}{subDirectory}{readingName}.json'):
        with open(f'.{subDirectory}data{subDirectory}{keysDictionary}{subDirectory}{readingName}.json', mode='w') as file:
            file.write('{\n"percentage" : "0%",\n"answers" : {}}')

    with open(f'.{subDirectory}data{subDirectory}{keysDictionary}{subDirectory}{readingName}.json', encoding='utf-8', mode='r+') as file:
        data = json.load(file)
        graspLength = driver.execute_script('var denom = $("[data-grasp]").length; return denom;')

        data['percentage'] = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text).replace(' correct', '')

        if data.get('answers') is None:
            data['answers'] = {}
        
        for a in range(graspLength):
            textbox = driver.find_element(By.XPATH, f'// textarea[@data-grasp="{a+1}"]')
            driver.execute_script("arguments[0].scrollIntoView();", textbox)

            if 'rgb(0, 128, 0)' in str(textbox.get_attribute('style')): #rgb(0, 128, 0) is the correct color indicator (green)
                if data['answers'].get(a+1) is None:
                    data['answers'][a+1] = str(textbox.text)
        save_file(file, data)