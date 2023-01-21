import requests, time, json, threading

from info import *
from web_driver import *

from pypresence import Presence

try:
    client_id = '993019974253822034'
    RPC = Presence(client_id)
    discordFound = False
    if discord_rpc == True:
        RPC.connect()
        discordFound = True
        RPCTime = int(time.time())
        RPC.update(large_image = "logo1", state = 'Starting up...', start = RPCTime)
except:
    discordFound = False

def get_mode(mode: str):
    global modes
    if loadWait(By.CLASS_NAME, 'ui-title'):
        title_elements = driver.find_elements(By.CLASS_NAME, 'ui-title')
        for a in range(len(title_elements)):
            for b in range(len(modes)):
                try:
                    if modes[b] in str(title_elements[a].text).lower() and mode != modes[b]:
                        return mode
                except:
                    pass
    else:
        if 'latin' not in str(driver.title):
            return mode

def get_assignment():
    global modes
    if loadWait(By.CLASS_NAME, 'ui-title'):
        title_elements = driver.find_elements(By.CLASS_NAME, 'ui-title')
        for a in range(len(title_elements)):
            for b in range(len(modes)):
                try:
                    if modes[b] in str(title_elements[a].text).lower():
                        return (str(str(driver.find_elements(By.CLASS_NAME, 'ui-title')[a].text).lower()).title()).split("'S ")[1]
                except:
                    pass
    else:
        if 'latin' not in str(driver.title):
            return None

def update_rpc():
    global discordFound
    mode = 'anything'

    while True:
        mode = get_mode(mode)
        assignment = get_assignment()
        RPCdetails = 'none'
        if mode == 'synopsis':
            if loadWait(By.XPATH, f"// h1[@class='showScore ui-title']"):
                score = driver.find_element(By.XPATH, f"// h1[@class='showScore ui-title']")
                if 'score' not in str(score.text):
                    RPCdetails = str(score.text)

        elif mode == '(grasp)' or mode == 'reading' or mode == 'composition':
            if loadWait(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']"):
                RPCdetails = str(driver.find_element(By.XPATH, f"// h3[@class='showScore ui-bar ui-bar-c ui-title']").text)

        elif mode == 'ciples' or mode == 'infinitive morphology':
            if loadWait(By.XPATH, f"// h3[@class='showScore ui-title']"):
                RPCdetails = '(' + str(assignment.split('(')[1])
                showScore = driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']")

                if str(showScore.text) != 'your score will appear here':
                    RPCdetails += ' / ' + str(showScore.text)
                assignment = str(assignment.split('(')[0])
        elif mode == 'noun-adj':
            if loadWait(By.XPATH, f"// h3[@class='showScore ui-title']"):
                showScore = driver.find_element(By.XPATH, f"// h3[@class='showScore ui-title']")

                if 'will appear here' not in str(showScore.text):
                    RPCdetails = str(str(showScore.text).split('\n')[0]).split('correctly. ')[1]

        if RPCdetails != 'none':
            RPC.update(large_image = "logo1", details = assignment, state = RPCdetails, start = RPCTime)
        elif RPCdetails == 'none':
            RPC.update(large_image = "logo1", details = assignment, start = RPCTime)
        time.sleep(1)

def rpc_start():
    threading.Thread(target=update_rpc).start()