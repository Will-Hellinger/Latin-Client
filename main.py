# ---------->SETUP START<----------
try:
    import time, pynput, sys, playsound, threading, random
    import glob
    import check_update
    from info import *
    from discord_rpc import *
    from web_driver import *
    import infinitive_morphology, noun_adj, synopsis, timed_morphology, timed_vocabulary, readings
except Exception as error:
    input(error)
    exit()

def debugger_tool():
    layout = [[sg.Text('Module:'), sg.Combo(['infinitive_morphology', 'noun_adj', 'synopsis', 'timed_morphology', 'timed_vocabulary', 'readings'], default_value='infinitive_morphology', key='_MODULE_INPUT_'), sg.Button("Reload")],
            [sg.Text('Injection Token:'), sg.Input(key='_TOKEN_INPUT_'), sg.Button("Inject")],
            [sg.Text('Token:'), sg.Input(key='_TOKEN_OUTPUT_'), sg.Button("Get Token")]]
    window = sg.Window('debugger', layout, resizable=True)

    while True:
        event, values = window.read()
        if event == 'Reload':
            module = values['_MODULE_INPUT_']

            if module == 'infinitive_morphology':
                importlib.reload(infinitive_morphology)
            elif module == 'noun_adj':
                importlib.reload(noun_adj)
            elif module == 'synopsis':
                importlib.reload(synopsis)
            elif module == 'timed_morphology':
                importlib.reload(timed_morphology)
            elif module == 'timed_vocabulary':
                importlib.reload(timed_vocabulary)
            elif module == 'readings':
                importlib.reload(readings)
        elif event == 'Inject':
            driver.execute_script(f'document.cookie = "PHPSESSID={values["_TOKEN_INPUT_"]}"')
            time.sleep(.5)
            driver.get("https://lthslatin.org/")
        elif event == 'Get Token':
            window.Element('_TOKEN_OUTPUT_').Update(str(get_token()))
        elif event == sg.WIN_CLOSED:
            break
    window.close()


update = False

## DEV TOOL
if len(sys.argv) >= 2:
    if str(sys.argv[1]) == '--debugger':
        update = False
        try:
            import PySimpleGUI as sg
            import importlib
            threading.Thread(target=debugger_tool).start()
        except Exception as error:
            print(f'unable to launch debugger due to {error}')


try:
    if update:
        check_update.run()
except Exception as error:
    print(f'unable to update due to {error}')

print(f'[+] Starting Client v{version}')

def get_token():
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['domain'] == 'lthslatin.org':
            token = cookie['value']
    return token

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

def heheHA():
    playsound.playsound(f'.{subDirectory}data{subDirectory}sounds{subDirectory}test.mp3')

try:
    if int(random.randint(1,50)) == 1 and funnySound == True:
        threading.Thread(target=heheHA).start()
except:
    pass

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
print(f'[+] Successfully Started Client v{version}')

#if discordFound:
#    rpc_start()

#load plugins
pluginFiles = glob.glob(f'.{subDirectory}data{subDirectory}plugins{subDirectory}*.plg')
plugins = []
for a in range(len(pluginFiles)):
    loadPlugin = True

    with open(pluginFiles[a], encoding='utf-8', mode='r') as file:
        try:
            pluginCode = (str(file.read()).replace('\n', '')).split('<code>')[1]
        except Exception as error:
            print(f'[-] plugin {pluginFiles[a]} couldnt be loaded, error: {error}')
            loadPlugin = False

    with open(pluginFiles[a], encoding='utf-8', mode='r') as file:
        try:
            pluginInfo = json.loads(str((str(file.read()).replace('\n', '')).split('<code>')[0]).replace('<info>', ''))
        except Exception as error:
            print(f'[-] plugin {pluginFiles[a]} couldnt be loaded, error: {error}')
            loadPlugin = False

    if loadPlugin == True:
        print(f"[+] Plugin: {pluginInfo.get('plugin-name')}, By: {pluginInfo.get('author-name')} loaded")
        plugins.append([pluginInfo["mode"], pluginCode])

while True:
    if loadWait(By.CLASS_NAME, 'ui-title'):
        title_elements = driver.find_elements(By.CLASS_NAME, 'ui-title')
        for a in range(len(title_elements)):
            for b in range(len(modes)):
                try:
                    if modes[b] in str(title_elements[a].text).lower() and mode != modes[b]:
                        mode = modes[b]
                except:
                    pass
    else:
        if 'latin' not in str(driver.title):
            break

    for a in range(len(plugins)):
        if mode == plugins[a][0]:
            driver.execute_script(plugins[a][1])

    if mode == 'launchpad':
        doAction = False
        enterKey = False
    elif mode == '(grasp)' or mode == 'reading':
        if doAction == True:
            try:
                readings.learn_words()
                readings.build_key()
            except Exception as error:
                print(f'error: {error}')
            doAction = False
    elif mode == 'noun-adj':
        if doAction == True:
            #Solves latin for you
            try:
                noun_adj.solver()
            except Exception as error:
                print(f'error: {error}')
                doAction = False
    elif mode == 'infinitive morphology' or mode == 'ciples':
        if enterKey == True:
            #Adds enter key back
            try:
                infinitive_morphology.enter_addon()
            except Exception as error:
                print(f'error: {error}')
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
            try:
                synopsis.solve()
            except Exception as error:
                print(f'error: {error}')
            doAction = False
    time.sleep(.1)
driver.close()
