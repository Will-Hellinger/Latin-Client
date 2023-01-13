# ---------->SETUP START<----------
try:
    import time, pynput
    from system_commands import *
    import heheHa
    import check_update
    from info import *
#    from discord_rpc import *
    from web_driver import *
    import infinitive_morphology, noun_adj, synopsis, timed_morphology, timed_vocabulary
except Exception as error:
    input(error)
    exit()

check_update.run()
print(f'[+] Starting Client v{version}')

def on_press(key):
    global doAction, actionButton, enterKey
    try:
        if key == pynput.keyboard.Key.enter:
            enterKey = True
        elif str(key.char) == actionButton:
            doAction = not doAction
    except:
        pass
listener = pynput.keyboard.Listener(on_press=on_press)
listener.start()

# ---------->SETUP END<----------

while True:
    try:
        driver.get(latinLink)
        print('[+] Successfully Connected to Schoology')
        break
    except:
        print('[-] Failed to Connect to Schoology')

while True:
    if loadWait(By.ID, 'edit-mail'):
        driver.find_element(By.ID, 'edit-mail').send_keys(schoologyUser)
    else:
        print('unable to find username input')
    if loadWait(By.ID, 'edit-pass'):
        driver.find_element(By.ID, 'edit-pass').send_keys(schoologyPass)
    else:
        print('unable to find password input')
    if loadWait(By.ID, 'edit-submit'):
        driver.find_element(By.ID, 'edit-submit').click()
    else:
        print('unable to click enter button')
    if loadWait(By.ID, 'schoology-app-container'):
        print('[+] Successfully Logged In')
        break
    else:
        print('[-] unable to log in, retrying')
        driver.get(latinLink)
time.sleep(3)
while True:
    try:
        driver.get('https://lthslatin.org')
        print('[+] Successfully Loaded LTHS Latin')
        break
    except:
        print('[-] Failed to load LTHS Latin, retying')

if loadWait(By.CLASS_NAME, 'ui-title'):
    user = str(str(str(driver.find_element(By.CLASS_NAME, 'ui-title').text).split("'s")[0]).lower()).title()
    print(f'[+] Located user: {user}')
else:
    print('[-] Unable to Find User')
mode = 'launchpad'
assignment = 'Latin Launchpad'
print(f'\033[1;32;40m[+] Successfully Started Client v{version}')

#rpc_start(user)

while True:
    if loadWait(By.CLASS_NAME, 'ui-title'):
        for a in range(len(driver.find_elements(By.CLASS_NAME, 'ui-title'))):
            for b in range(len(modes)):
                try:
                    if modes[b] in str(driver.find_elements(By.CLASS_NAME, 'ui-title')[a].text).lower():
                        if mode != modes[b]:
                            mode = modes[b]
                except:
                    pass
    else:
        if 'latin' not in str(driver.title):
            break
    if mode == 'launchpad':
        doAction = False
        enterKey = False
    if mode == 'noun-adj':
        if doAction == True:
            #Solves latin for you
            noun_adj.solver()
    elif mode == 'infinitive morphology' or mode == 'ciples':
        if enterKey == True:
            #Adds enter key back
            infinitive_morphology.enter_addon()
            enterKey = False
    elif mode == 'timed morphology':
        if doAction == True:
            try:
                timed_morphology.solver()
            except Exception as error:
                print(f'error: {error}')
                doAction = False
    elif mode == 'timed vocabulary':
        if doAction == True:
            try:
                timed_vocabulary.solver()
            except Exception as error:
                print(f'error: {error}')
                doAction = False
    elif mode == 'synopsis':
        if doAction:
            #Finds latin conjugation type
            try:
                synopsis.find_chart()
            except Exception as error:
                print(f'error: {error}')
            doAction = False
driver.close()
