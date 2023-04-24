# ---------->SETUP START<----------
try:
    import time, pynput, sys, playsound, threading, random
    import glob
    import updater
    from info import *
    from discord_rpc import *
    from web_driver import *
    import infinitive_morphology, noun_adj, synopsis, timed_morphology, timed_vocabulary, readings, compositions
except Exception as error:
    input(error)
    exit()

update = True

def debugger_tool():
    module_strings = ['infinitive_morphology', 'noun_adj', 'synopsis', 'timed_morphology', 'timed_vocabulary', 'readings', 'compositions']

    layout = [[sg.Text('Module:'), sg.Combo(module_strings, default_value='infinitive_morphology', key='_MODULE_INPUT_'), sg.Button("Reload")],
            [sg.Text('Injection Token:'), sg.Input(key='_TOKEN_INPUT_'), sg.Button("Inject")],
            [sg.Text('Token:'), sg.Input(key='_TOKEN_OUTPUT_'), sg.Button("Get Token")]]
    window = sg.Window('debugger', layout, resizable=True)

    while True:
        event, values = window.read()
        if event == 'Reload':
            module = values['_MODULE_INPUT_']

            modules = (infinitive_morphology, noun_adj, synopsis, timed_morphology, timed_vocabulary, readings, compositions)
            
            if module_strings.index(module) != -1:
                importlib.reload(modules[module_strings.index(module)])
            
        elif event == 'Inject':
            driver.execute_script(f'document.cookie = "PHPSESSID={values["_TOKEN_INPUT_"]}"')
            time.sleep(.5)
            driver.get("https://lthslatin.org/")
        elif event == 'Get Token':
            window.Element('_TOKEN_OUTPUT_').Update(str(get_token()))
        elif event == sg.WIN_CLOSED:
            break
    window.close()

## DEV TOOL
if len(sys.argv) >= 2:
    if str(sys.argv[1]) == '--debugger':
        update = False
        
        start_time = time.time()
        updater.build_chksm()
        print(f'finished in {time.time() - start_time}')

        try:
            import PySimpleGUI as sg
            import importlib
            threading.Thread(target=debugger_tool).start()
        except Exception as error:
            print(f'unable to launch debugger due to {error}')


try:
    if updater.check_update() and update == True:
        updater.update()
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

#best to keep this on a seperate thread lol
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

discord_found = check_discord()

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

        for element in title_elements:
            for available_mode in modes:
                try:
                    if available_mode in str(element.text).lower():
                        assignment = str(element.text).lower().replace(f"{user.lower()}'s ", "")
                        if available_mode != mode:
                            mode = available_mode
                        
                        if discord_found:
                            update_rpc(mode, assignment)
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
            
    elif mode == 'translation':
        if doAction == True:
            try:
                readings.learn_words()
            except Exception as error:
                print(f'error: {error}')
            doAction = False
    
    elif mode == 'composition':
        if doAction == True:
            try:
                compositions.solve()
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
        if doAction == True:
            try:
                synopsis.solve()
            except Exception as error:
                print(f'error: {error}')
            doAction = False
    
    time.sleep(.1)
driver.close()