import json
import os
from pathlib import Path

if os.name == 'nt':
    subDirectory = '\\'
    pip = 'pip'
    clear = 'cls'
else:
    subDirectory = '/'
    pip = 'pip3'
    clear = 'clear'

def build_dictionary():
    filelist = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if str(os.path.join(root,file)).endswith('.json') and 'latin_dictionary' in str(os.path.join(root,file)):
                filelist.append(os.path.join(root,file))


def translate(word: str, translationDict: list, wordDict: list):
    translated = []
    for a in range(len(wordDict)):
        if wordDict[a] == word:
            translated.append(translationDict[a])
    return translated

filelist = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if str(os.path.join(root,file)).endswith('.json') and 'latin_dictionary' in str(os.path.join(root,file)):
            filelist.append(os.path.join(root,file))

allLatinWords = []
for a in range(len(filelist)):
    latinWord = str(filelist[a].split(subDirectory)[len(filelist[a].split(subDirectory)) - 1]) #Getting Word from filename
    latinWord = latinWord.replace('.json', '').replace('^', '\\').replace('_', ' ').encode('utf-8').decode('unicode-escape') #cleaning up word
    allLatinWords.append(latinWord)

englishWords = []
latinWords = []
for a in range(len(filelist)):
    with open(filelist[a], 'r') as file:
        data = json.load(file)
        for item in data:
            if data[item] == True:
                englishWords.append(item)
                latinWords.append(allLatinWords[a])

englishInput = str(input('')).replace(',', '').replace('.', '').split(' ')
englishOutput = []

for a in range(len(englishInput)):
    temp = []
    if a != len(englishInput) - 1:
        if englishInput[a] in englishWords:
            temp.append(englishInput[a])
        if englishInput[a] + " " + englishInput[a+1] in englishWords:
            temp.append(f'{englishInput[a]} {englishInput[a+1]}')
    elif a == len(englishInput) - 1:
        if englishInput[a] in englishWords:
            temp.append(englishInput[a])

    if len(temp) >= 1:
        temp = max(temp, key=len)
        if len(temp.split(' ')) >= 2:
            for b in range(len(temp.split(' '))):
                englishInput[englishInput.index(temp.split(' ')[b])] = 'fs;falsdkfjaslkdj'
        else:
            englishInput[englishInput.index(temp)] = 'fs;falsdkfjaslkdj'
        englishOutput.append(temp)


print(englishOutput)
for a in range(len(englishOutput)):
    print(translate(englishOutput[a], latinWords, englishWords))