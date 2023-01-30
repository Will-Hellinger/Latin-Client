from web_driver import *
import json, time
from info import *

dictionary = 'latin_dictionary'

def save_file(file: bytes, data: dict):
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()

def scanforWord(list, word):
    for a in range(len(list)):
        if list[a].text == word:
            return True
    return False

def scan_words():
    latin_words = driver.find_elements(By.XPATH, '// span[@class="tappit latin"]')
    newWords = []
    print('prepping elements...', end='\r')
    for a in range(len(latin_words)):
        file_name = (str(str(latin_words[a].text).replace(" ", "_")).encode("unicode-escape")).decode("utf-8").replace("\\", "^")

        #This is honestly only for windows
        removeList = ['\\', '?', '%', '*', ':', '|', '"', '<', '>']
        replaceList = ['(bs)', '(qm)', '(ps)', '(a)', '(c)', '(p)', '(qm)', '(fa)', '(ba)']
        for b in range(len(removeList)):
            file_name = file_name.replace(str(removeList[b]), str(replaceList[b]))

        if not os.path.exists(f'.{subDirectory}data{subDirectory}latin_dictionary{subDirectory}{file_name}.json'):
            newWords.append(latin_words[a])
        else:
            with open(f'.{subDirectory}data{subDirectory}latin_dictionary{subDirectory}{file_name}.json', mode='r+') as file:
                wordData = json.load(file)
            if len(wordData) == 0:
                newWords.append(latin_words[a])

    duplicateFree = []
  
    for a in range(len(newWords)):
        if not scanforWord(duplicateFree, newWords[a].text):
            duplicateFree.append(newWords[a])

    latin_words = duplicateFree

    for a in range(len(latin_words)):
        print(f'Scanning: {round((100/len(latin_words))*(a+1))}%       ', end='\r')
        driver.execute_script("arguments[0].scrollIntoView();", latin_words[a])
        file_name = (str(str(latin_words[a].text).replace(" ", "_")).encode("unicode-escape")).decode("utf-8").replace("\\", "^")

        #This is honestly only for windows
        removeList = ['\\', '?', '%', '*', ':', '|', '"', '<', '>']
        replaceList = ['(bs)', '(qm)', '(ps)', '(a)', '(c)', '(p)', '(qm)', '(fa)', '(ba)']
        for b in range(len(removeList)):
            file_name = file_name.replace(str(removeList[b]), str(replaceList[b]))
        if not os.path.exists(f'.{subDirectory}data{subDirectory}latin_dictionary{subDirectory}{file_name}.json'):
            with open(f'.{subDirectory}data{subDirectory}latin_dictionary{subDirectory}{file_name}.json', mode='w') as file:
                file.write('{\n}')

        with open(f'.{subDirectory}data{subDirectory}latin_dictionary{subDirectory}{file_name}.json', mode='r+') as file:
            data = json.load(file)
            latin_words[a].click()
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
    print('Done Scanning ')
