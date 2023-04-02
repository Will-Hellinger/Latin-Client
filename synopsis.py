from web_driver import *
from info import *
import json
import pyinflect
import unicodedata
import re


conjugationChartKey = json.load(open(f'.{subDirectory}data{subDirectory}conjugation_chart_types.json'))
blocks = ('e', 'b', 'c', 'd')

conjugationNames = list(conjugationChartKey.keys())
totalConjugations = list(conjugationChartKey.values())


def showHiddenDropdowns():
    nontoucheddropDowns = driver.find_elements(By.XPATH, f"// div[@class='ui-collapsible-content ui-body-inherit ui-collapsible-content-collapsed']")
    toucheddropDowns = driver.find_elements(By.XPATH, f"// div[@class='ui-collapsible-heading ui-collapsible-content-collapsed']")
    dropDowns = nontoucheddropDowns + toucheddropDowns
    for a in range(len(dropDowns)):
        newClass = 'ui-collapsible-heading'
        driver.execute_script(f"arguments[0].setAttribute('class','{newClass}')", dropDowns[a])


def hideShownDropdowns():
    toucheddropDowns = driver.find_elements(By.XPATH, f"// div[@class='ui-collapsible-content ui-body-inherit']")
    nontoucheddropDowns = driver.find_elements(By.XPATH, f"// div[@class='ui-collapsible-heading']")
    dropDowns = nontoucheddropDowns + toucheddropDowns
    for a in range(len(dropDowns)):
        newClass = 'ui-collapsible-heading ui-collapsible-content-collapsed'
        driver.execute_script(f"arguments[0].setAttribute('class','{newClass}')", dropDowns[a])


def find_word(element_list: list):
    for a in range(len(element_list)):
        if str(element_list[a].text) != '':
            return str(element_list[a].text)
    return ''


def strip_accents(text):
    return ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')


def find_details():
    global conjugationNames, totalConjugations, blocks
    #Finds latin conjugation type
    chart = 'first' # temp
    chartBackup = []
    chartFound = False

    latinWords = []
    for a in range(len(blocks)):
        try:
            latinWords.append(find_word(driver.find_elements(By.XPATH, f"// span[@class='ui-body ui-body-{str(blocks[a])} latin']")))
        except:
            latinWords.append(f'unable to get word {a}')

    for a in range(len(totalConjugations)):
        tempchartFound = True
        count = 0
        for b in range(len(totalConjugations[a])):
            if latinWords[b].endswith(totalConjugations[a][b]):
                count += 1
            elif not latinWords[b].endswith(totalConjugations[a][b]):
                tempchartFound = False
        if tempchartFound == True:
            chart = conjugationNames[a]
            chartFound = True
        chartBackup.append(count)
    
    if chartFound == False:
        chart = conjugationNames[chartBackup.index(max(chartBackup))] #this is a fallback in case it cant find the chart regularly

    english_word = find_word(driver.find_elements(By.XPATH, f"// li[@class='ui-block-e']")).split(' |')[0]
    tense = find_word(driver.find_elements(By.XPATH, f"// li[@class='ui-block-e']")).split('| ')[1]

    #VB - Verb, Base Form
    #VBD - Verb, Past Tense
    #VBG - Verb, Gerund or Present Participle
    #VBN - Verb, Past Participle
    #VBZ - Verb, 3rd Person Singular Present

    english_words = {"VB": english_word, 
                     "VBG" : pyinflect.getInflection(english_word, 'VBG')[0],
                     "VBN" : pyinflect.getInflection(english_word, 'VBN')[0],
                     "VBZ" : pyinflect.getInflection(english_word, 'VBZ')[0],
                     "VBD" : pyinflect.getInflection(english_word, 'VBD')[0]}

    output = {"chart" : chart,
            "latin words" : latinWords,
            "english words" : english_words,
            "tense" : tense}

    return output


def solve():
    global blocks

    hideShownDropdowns()
    
    currentModeElement = driver.find_element(By.XPATH, f"// div[@class='ui-page ui-page-theme-a ui-page-footer-fixed ui-page-active']")
    pageData = find_word(currentModeElement.find_elements(By.XPATH, f"// div[@class='ui-grid-a ui-responsive']")).replace('\nclick to expand contents', '')

    pageInputs = []
    temp = currentModeElement.find_elements(By.TAG_NAME, f"input")
    for a in range(len(temp)):
        pageInputs.append(str(temp[a].get_attribute('id')))

    currentMode = pageData.split('\n')[0]
    details = find_details()

    latinDict = json.load(open(f'.{subDirectory}data{subDirectory}latin-conjugation-charts{subDirectory}{details["chart"]}.json'))

    dictTense = str(details["tense"]).replace('1st ', 'first-').replace('2nd ', 'second-').replace('3rd ', 'third-')
    englishDict = json.load(open(f'.{subDirectory}data{subDirectory}english-conjugation-charts{subDirectory}{dictTense}.json'))

    if currentMode == '' and 'storeScore' in pageData:
        return None
    
    if currentMode == 'PRESENT IMPERATIVE ACTIVE' or currentMode == 'PRESENT IMPERATIVE PASSIVE':
        currentMode = 'IMPERATIVES'

    pageData = str(pageData.replace(f'{currentMode}\n', ''))
    pageData = str(pageData.replace(f'future perfect', 'future-perfect'))
    pageData = pageData.split('\n')

    if currentMode == 'SUBJUNCTIVE':
        currentMode = 'SUBJUNCTIVES'

    latinInputDict = {}
    englishInputDict = {}

    if currentMode != 'IMPERATIVES':
        mode = 'none'
        for a in range(len(pageData)):
            if pageData[a].upper() == 'ACTIVE' or pageData[a].upper() == 'PASSIVE':
                mode = pageData[a].upper()
            else:
                latinInputDict[f'{mode} {pageData[a].upper()}'] = 'temp'
                if currentMode != 'SUBJUNCTIVES':
                    englishInputDict[f'{mode} {pageData[a].upper()}'] = 'temp'

    elif currentMode == 'IMPERATIVES':
        latinInputDict = {"ACTIVE SINGULAR" : "temp",
                          "ACTIVE PLURAL" : "temp",
                          "PASSIVE SINGULAR" : "temp",
                          "PASSIVE PLURAL" : "temp"}
        englishInputDict = {"ACTIVE" : "temp",
                            "PASSIVE" : "temp"}

    latinTemp = []
    englishTemp = []
    for a in range(len(pageInputs)):
        if 'english' not in driver.find_element(By.XPATH, f"// input[@id='{pageInputs[a]}']").get_attribute('class'):
            latinTemp.append(pageInputs[a])
        else:
            englishTemp.append(pageInputs[a])

    latinInputDictKeys = list(latinInputDict.keys())
    englishInputDictKeys = list(englishInputDict.keys())

    for a in range(len(latinInputDictKeys)):
        latinInputDict[latinInputDictKeys[a]] = latinTemp[a]
    for a in range(len(englishInputDictKeys)):
        englishInputDict[englishInputDictKeys[a]] = englishTemp[a]

    hideShownDropdowns()
    showHiddenDropdowns()

    for item in latinInputDict:
        latinInput = driver.find_element(By.XPATH, f"// input[@id='{latinInputDict[item]}']")
        driver.execute_script("arguments[0].scrollIntoView();", latinInput)

        activeness = str(item).split(' ')[0]
        tense = str(item).split(' ')[1]

        data_theme = blocks.index(latinInput.get_attribute('data-theme'))

        word = details["latin words"][data_theme]
        wordEnding = conjugationChartKey[details["chart"]][data_theme]

        newEnding = latinDict[currentMode.upper()[:-1]][activeness][tense]
        if currentMode == 'INDICATIVES' or currentMode == 'SUBJUNCTIVES':
            newEnding = newEnding[details['tense']]

        ignoreWords = ['dic', 'dac', 'fic', 'fuc'] #little rhyme lol
        endlessWord = re.sub(f'{strip_accents(wordEnding)}$', '', strip_accents(word))

        if newEnding == "" and endlessWord not in ignoreWords:
            newEnding = wordEnding[0]

        answer = re.sub(f'{strip_accents(wordEnding)}$', newEnding, strip_accents(word))

        if 'rgb(255, 0, 0)' in str(latinInput.get_attribute('style')):
            latinInput.clear()

        if loadWait(By.XPATH, f"// input[@id='{latinInputDict[item]}']") and 'rgb(0, 128, 0)' not in str(latinInput.get_attribute('style')):
            latinInput.send_keys(answer)
            latinInput.send_keys(Keys.RETURN)
    
    hideShownDropdowns()
    showHiddenDropdowns()

    for item in englishInputDict:
        englishInput = driver.find_element(By.XPATH, f"// input[@id='{englishInputDict[item]}']")
        driver.execute_script("arguments[0].scrollIntoView();", englishInput)

        activeness = str(item).split(' ')[0]

        answer = englishDict[currentMode.upper()[:-1]][activeness]

        if currentMode.upper() != 'IMPERATIVES':
            tense = str(item).split(' ')[1]
            answer = answer[tense]
        
        verbs = details['english words']

        replaceVerbs = ['*VB*', '*VBG*', '*VBN*', '*VBZ*', '*VBD*']
        for a in range(len(replaceVerbs)):
            answer = answer.replace(replaceVerbs[a], verbs[replaceVerbs[a].replace('*', '')])

        if 'rgb(255, 0, 0)' in str(englishInput.get_attribute('style')):
            englishInput.clear()

        if loadWait(By.XPATH, f"// input[@id='{englishInputDict[item]}']") and 'rgb(0, 128, 0)' not in str(englishInput.get_attribute('style')):
            englishInput.send_keys(answer)
            englishInput.send_keys(Keys.RETURN)