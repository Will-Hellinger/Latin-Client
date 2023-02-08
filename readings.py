from web_driver import *
import json, time
from info import *

dictionary = 'latin_dictionary'

def save_file(file: bytes, data: dict):
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()


def encode_word(word: str):
    encodedWord = (str(word.replace(" ", "_")).encode("unicode-escape")).decode("utf-8").replace("\\", "^")

    #This is honestly only for windows
    removeList = ['\\', '?', '%', '*', ':', '|', '"', '<', '>']
    replaceList = ['(bs)', '(qm)', '(ps)', '(a)', '(c)', '(p)', '(qm)', '(fa)', '(ba)']
    for b in range(len(removeList)):
        encodedWord = encodedWord.replace(str(removeList[b]), str(replaceList[b]))
    
    return encodedWord


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
        file_name = encode_word(latinWordTexts[a][1])

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
        file_name = encode_word(latinWords[a].text)

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
