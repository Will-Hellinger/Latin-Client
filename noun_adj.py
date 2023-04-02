from web_driver import *
from info import *
import time, random, json

def load_chart():
    with open(f".{subDirectory}data{subDirectory}noun-adj_chart.json", encoding='utf-8') as file:
        data = json.load(file)
        allEndings = []
        for item in data:
            allEndings.append([item, data[item]])
    return allEndings

def solver():
    allEndings = load_chart()
    nouns = []
    for a in range(10):
        if loadWait(By.NAME, f'input{str(a+1)}'):
            nouns.append((driver.find_element(By.NAME, f'input{str(a+1)}').text).split('\n')[0])
            
    for a in range(len(nouns)):
        if 'noun' not in str(driver.title).lower():
            break

        words = nouns[a].split(' ')
        availableEndings = []
        unknownWord = False
        output = False

        for b in range(len(words)):
            tempList = []
            for c in range(len(allEndings)):
                if words[b].endswith(allEndings[c][0]):
                    tempList.append(allEndings[c][0])
            if tempList != []:
                availableEndings.append(tempList)

        try:
            for b in range(len(availableEndings)):
                if len(availableEndings[b]) != 0:
                    availableEndings[b] = max(availableEndings[b], key=len)
                else:
                    unknownWord = True
        except:
            unknownWord = True
                
        if unknownWord == False:
            endingNumbers = []
            for b in range(len(availableEndings)):
                for c in range(len(allEndings)):
                    if availableEndings[b] == allEndings[c][0]:
                        endingNumbers.append(allEndings[c][1])
            for b in range(len(endingNumbers[0])):
                if endingNumbers[0][b] in endingNumbers[1]:
                    output = True

        try:
            if a != 0:
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, f'// label[@for="no{a}"]'))
            else:
                driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.HOME)
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, f'// label[@for="no1"]'))
        except:
            print(f'unable to scroll to element {a}')


        if 'noun' not in str(driver.title).lower():
            break

        choice = 'no'
        if output == True:
            choice = 'yes'
        
        try:
            if loadWait(By.XPATH, f'// label[@for="{choice}{a+1}"]'):
                driver.find_element(By.XPATH, f'// label[@for="{choice}{a+1}"]').click()
        except:
            print(f'unable to press {choice}{a+1}')


        if human_mode == True:
            time.sleep(int(random.randint(100, 500))/100)


    selection = 'agreeSubmit'

    while True:
        if 'noun' not in str(driver.title).lower():
            break

        try:
            if loadWait(By.ID, selection):
                driver.find_element(By.ID, selection).click()
                if selection != 'agreeMore':
                    selection = 'agreeMore'
                else:
                    break
        except:
            print(f'unable to press get {selection}')
            time.sleep(2)

    time.sleep(5)

    try:
        print(str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text).split('\n')[0])
    except:
        print('unable to get score')