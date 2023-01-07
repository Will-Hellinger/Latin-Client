from web_driver import *

def find_chart():
    #Finds latin conjugation type
    conjugationNames = ['first', 'second', 'third', 'thirdI', 'fourth']
    totalConjugations = [['ō', 'āre', 'vī', 'us'], ['eō', 'ēre', 'ī', 'us'], ['ō', 'ere', 'ī', 'us'], ['iō', 'ere', 'ī', 'us'], ['iō', 'īre', 'ī', 'us']]
    latinWords = []
    blocks = ['e', 'b', 'c', 'd']
    for a in range(len(blocks)):
        try:
            latinWords.append(driver.find_element(By.XPATH, f"// span[@class='ui-body ui-body-{str(blocks[a])} latin']").text)
        except:
            latinWords.append(f'unable to get word {a}')
    print(latinWords)
    outputChoice = []
    for a in range(len(totalConjugations)):
        for b in range(4):
            if totalConjugations[a][b] not in latinWords[b]:
                continue
            outputChoice.append(totalConjugations[a])
    numberCount = []
    for a in range(len(outputChoice)):
        tempText = ''
        for b in range(len(outputChoice[a])):
            tempText += outputChoice[a][b]
        numberCount.append(len(tempText))
    print(conjugationNames[totalConjugations.index(outputChoice[numberCount.index(max(numberCount))])])
    print((driver.find_element(By.XPATH, f"// li[@class='ui-block-e']").text).split(' |')[0])
    print((driver.find_element(By.XPATH, f"// li[@class='ui-block-e']").text).split('| ')[1])