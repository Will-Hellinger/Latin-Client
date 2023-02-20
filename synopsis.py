from web_driver import *
from info import *
import json
import time
import unicodedata
import re


conjugationChartKey = json.load(open(f'.{subDirectory}data{subDirectory}conjugation_chart_types.json'))

conjugationNames = []
for item in conjugationChartKey:
    conjugationNames.append(str(item))

totalConjugations = []
for item in conjugationChartKey:
    totalConjugations.append(conjugationChartKey[str(item)])


def showHiddenDropdowns():
    nontoucheddropDowns = driver.find_elements(By.XPATH, f"// div[@class='ui-collapsible-content ui-body-inherit ui-collapsible-content-collapsed']")
    toucheddropDowns = driver.find_elements(By.XPATH, f"// div[@class='ui-collapsible-heading ui-collapsible-content-collapsed']")
    dropDowns = nontoucheddropDowns + toucheddropDowns
    for a in range(len(dropDowns)):
        newClass = 'ui-collapsible-heading'
        driver.execute_script(f"arguments[0].setAttribute('class','{newClass}')", dropDowns[a])


def find_word(element_list: list):
    for a in range(len(element_list)):
        if str(element_list[a].text) != '':
            return str(element_list[a].text)
    return ''


def strip_accents(text):
    return ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')


def find_details():
    global conjugationNames, totalConjugations
    #Finds latin conjugation type
    chart = 'first' # temp

    latinWords = []
    blocks = ['e', 'b', 'c', 'd']
    for a in range(len(blocks)):
        try:
            latinWords.append(find_word(driver.find_elements(By.XPATH, f"// span[@class='ui-body ui-body-{str(blocks[a])} latin']")))
        except:
            latinWords.append(f'unable to get word {a}')

    for a in range(len(totalConjugations)):
        chartFound = True
        for b in range(len(totalConjugations[a])):
            if not latinWords[b].endswith(totalConjugations[a][b]):
                chartFound = False
        if chartFound == True:
            chart = conjugationNames[a]

    english_word = find_word(driver.find_elements(By.XPATH, f"// li[@class='ui-block-e']")).split(' |')[0]
    tense = find_word(driver.find_elements(By.XPATH, f"// li[@class='ui-block-e']")).split('| ')[1]

    output = {"chart" : chart,
            "latin words" : latinWords,
            "english word" : english_word,
            "tense" : tense}

    return output


def solve():
    currentModeElement = driver.find_element(By.XPATH, f"// div[@class='ui-page ui-page-theme-a ui-page-footer-fixed ui-page-active']")
    pageData = find_word(currentModeElement.find_elements(By.XPATH, f"// div[@class='ui-grid-a ui-responsive']")).replace('\nclick to expand contents', '')

    pageInputs = []
    temp = currentModeElement.find_elements(By.TAG_NAME, f"input")
    for a in range(len(temp)):
        pageInputs.append(str(temp[a].get_attribute('id')))

    currentMode = pageData.split('\n')[0]
    details = find_details()

    dict = json.load(open(f'.{subDirectory}data{subDirectory}conjugation-charts{subDirectory}{details["chart"]}.json'))

    if currentMode == '' and 'storeScore' in pageData:
        return None
    
    if currentMode == 'PRESENT IMPERATIVE ACTIVE' or currentMode == 'PRESENT IMPERATIVE PASSIVE':
        currentMode = 'IMPERATIVES'

    pageData = str(pageData.replace(f'{currentMode}\n', ''))
    pageData = str(pageData.replace(f'future perfect', 'future-perfect'))
    pageData = pageData.split('\n')

    if currentMode == 'SUBJUNCTIVE':
        currentMode = 'SUBJUNCTIVES'

    showHiddenDropdowns()

    latinInputDict = {}
    print(currentMode)

    if currentMode != 'IMPERATIVES':
        mode = 'none'
        for a in range(len(pageData)):

            if pageData[a] == 'ACTIVE':
                mode = 'ACTIVE'
            elif pageData[a] == 'PASSIVE':
                mode = 'PASSIVE'
            else:
                latinInputDict[f'{mode} {pageData[a].upper()}'] = 'temp'
    else:
        latinInputDict = {"ACTIVE SINGULAR" : "temp",
                          "ACTIVE PLURAL" : "temp",
                          "PASSIVE SINGULAR" : "temp",
                          "PASSIVE PLURAL" : "temp"}

    temp = []
    for a in range(len(pageInputs)):
        if 'english' not in driver.find_element(By.XPATH, f"// input[@id='{pageInputs[a]}']").get_attribute('class'):
            temp.append(pageInputs[a])

    index = 0
    for item in latinInputDict:
        latinInputDict[item] = temp[index]
        index += 1

    index = 0
    for item in latinInputDict:
        latinInput = driver.find_element(By.XPATH, f"// input[@id='{latinInputDict[item]}']")
        driver.execute_script("arguments[0].scrollIntoView();", latinInput)

        activeness = str(item).split(' ')[0]
        tense = str(item).split(' ')[1]

        if latinInput.get_attribute('data-theme') == 'e':
            word = details["latin words"][0]
            wordEnding = conjugationChartKey[details["chart"]][0]
        elif latinInput.get_attribute('data-theme') == 'b':
            word = details["latin words"][1]
            wordEnding = conjugationChartKey[details["chart"]][1]
        elif latinInput.get_attribute('data-theme') == 'c':
            word = details["latin words"][2]
            wordEnding = conjugationChartKey[details["chart"]][2]
        elif latinInput.get_attribute('data-theme') == 'd':
            word = details["latin words"][3]
            wordEnding = conjugationChartKey[details["chart"]][3]

        newEnding = dict[currentMode.upper()[:-1]][activeness][tense]
        if currentMode == 'INDICATIVES' or currentMode == 'SUBJUNCTIVES':
            newEnding = newEnding[details['tense']]

        ignoreWords = ['dic', 'dac', 'fic', 'fuc']
        endlessWord = re.sub(f'{strip_accents(wordEnding)}$', '', strip_accents(word))

        if newEnding == "" and endlessWord not in ignoreWords:
            newEnding = wordEnding[0]

        answer = re.sub(f'{strip_accents(wordEnding)}$', newEnding, strip_accents(word))

        if loadWait(By.XPATH, f"// input[@id='{latinInputDict[item]}']"):
            latinInput.send_keys(answer)
            latinInput.send_keys(Keys.RETURN)

        index += 1