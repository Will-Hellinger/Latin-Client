from web_driver import *
from info import *
import time
import json
import os


noun_adj_chart = f'.{subDirectory}data{subDirectory}noun_adj_charts{subDirectory}{noun_adj_chart_name}.json'


def prediction(words: list = None) -> bool:
    """
    Predict if a given list of words forms a valid combination based on available endings.

    :param words: A list of words to predict.
    :return: True if a valid combination is predicted, otherwise False.
    """

    if len(words) != 2 or words is None:
        return False

    data = json.load(open(noun_adj_chart, mode='r', encoding='utf-8'))
    endings = []

    for word in words:
        all_endings = []

        for end in data:
            if word.endswith(end):
                all_endings.append(end)

        if len(all_endings) >= 1:
            endings.append(max(all_endings, key=len))
    
    if len(endings) <= 1:
        return False

    if endings[0] in data.get(endings[1]) or endings[1] in data.get(endings[0]):
        return True
    
    return False


def solver() -> None:
    """`
    Perform a series of actions, including solving word combinations and managing responses.

    :return: None
    """
    
    nouns = []

    for a in range(10):
        if loadWait(By.NAME, f'input{str(a+1)}'):
            nouns.append((driver.find_element(By.NAME, f'input{str(a+1)}').text).split('\n')[0])
    
    for a in range(len(nouns)):
        if 'noun' not in str(driver.title).lower():
            break

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

        words = nouns[a].split(' ')
        output = prediction(words)

        choice = 'no'
        if output == True:
            choice = 'yes'
        
        try:
            if loadWait(By.XPATH, f'// label[@for="{choice}{a+1}"]'):
                driver.find_element(By.XPATH, f'// label[@for="{choice}{a+1}"]').click()
        except:
            print(f'unable to press {choice}{a+1}')

        human_timeout(1000, 5000)

    selections = ['agreeSubmit', 'agreeMore']

    for selection in selections:
        while True:
            if 'noun' not in str(driver.title).lower():
                break

            try:
                if not loadWait(By.ID, selection):
                    break
                    
                driver.find_element(By.ID, selection).click()
                break
            except:
                print(f'unable to press get {selection}')
                time.sleep(2)

    time.sleep(5)

    response_text = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text).split('\n')[0]
    correct_amount = str(response_text.split(' out of ')[0])
    correct_amount = int(correct_amount.replace('You answered ', ''))

    try:
        print(f'{response_text}')
    except:
        print('unable to get score')