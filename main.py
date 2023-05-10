# ---------->SETUP START<----------
try:
    import time
    import pynput
    import sys
    import playsound
    import threading
    import random
    import glob
    from multiprocessing import Process
    from multiprocessing import Event
    import updater
    from info import *
    from discord_rpc import *
    from web_driver import *

    import infinitive_morphology, noun_adj, synopsis, timed_morphology, timed_vocabulary, readings, compositions, catullus #custom modules
except Exception as error:
    input(error)
    exit()

update = True
login_skip = False

def spoofer():
    while True:
        delay = random.randint(1000, 1500)/100

        spoof_activity(driver, 'grasp')
        time.sleep(delay)


def debugger_tool():
    spoof_active = False
    module_strings = ['infinitive_morphology', 'noun_adj', 'synopsis', 'timed_morphology', 'timed_vocabulary', 'readings', 'compositions', 'catullus']

    layout = [[sg.Text('Module:'), sg.Combo(module_strings, default_value='infinitive_morphology', key='_MODULE_INPUT_'), sg.Button("Reload")],
            [sg.Text('Injection Token:'), sg.Input(key='_TOKEN_INPUT_'), sg.Button("Inject")],
            [sg.Text('Token:'), sg.Input(key='_TOKEN_OUTPUT_'), sg.Button("Get Token")],
            [sg.Button("Reload Settings")], 
            [sg.Button("Spoof Activity"), sg.Text('Active: False', key='_SPOOF_ACTIVITY_MONITOR_')]]
    window = sg.Window('debugger', layout, resizable=True)

    while True:
        event, values = window.read()
        match event:
            case 'Reload':
                start_time = time.time()

                module = values['_MODULE_INPUT_']
                modules = (infinitive_morphology, noun_adj, synopsis, timed_morphology, timed_vocabulary, readings, compositions, catullus)
            
                if module in module_strings:
                    importlib.reload(modules[module_strings.index(module)])
            
                updater.build_chksm()
                print(f'finished in {time.time() - start_time}')
            
            case 'Inject':
                driver.execute_script(f'document.cookie = "PHPSESSID={values["_TOKEN_INPUT_"]}"')
                time.sleep(.5)
                driver.get("https://lthslatin.org/")
            
            case 'Get Token':
                window.Element('_TOKEN_OUTPUT_').Update(str(get_token()))
            
            case 'Reload Settings':
                load_settings()

            case 'Spoof Activity':
                spoof_active = not spoof_active

                window.Element('_SPOOF_ACTIVITY_MONITOR_').Update(f'Active: {spoof_active}')

                if spoof_active == True:
                    process = Process(target=spoofer)
                    process.start()
                elif spoof_active == False:
                    process.kill()
            
            case sg.WIN_CLOSED:
                break
    window.close()

## DEV TOOL
if '--debugger' in (sys.argv):
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
    
if '--login' in (sys.argv):
    login_skip = True

    driver.get("https://lthslatin.org/")
    driver.execute_script(f'document.cookie = "PHPSESSID={str(sys.argv[sys.argv.index("--login") + 1])}"')
    driver.get("https://lthslatin.org/")


try:
    if updater.check_update() and update == True:
        updater.update()
except Exception as error:
    print(f'unable to update due to {error}')

print(f'[+] Starting Client v{version}')


def wait_till(by=None, type=None, keys="", click=False, get_link=""):
    while True:
        try:
            if get_link != "":
                driver.get(get_link)
                break

            if by is not None and type is not None and loadWait(by, type):
                if click == True:
                    driver.find_element(by, type).click()
                elif keys != "":
                    driver.find_element(by, type).send_keys(keys)
                
                break
        except:
            time.sleep(.1)


def get_token():
    token = None
    
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

if login_skip == False:
    wait_till(get_link=latinLink)
    wait_till(by=By.ID, type='edit-mail', keys=schoologyUser)
    wait_till(by=By.ID, type='edit-pass', keys=schoologyPass)
    wait_till(by=By.ID, type='edit-submit', click=True)
    wait_till(by=By.ID, type='schoology-app-container')

time.sleep(3)

while True:
    try:
        driver.get('https://lthslatin.org')
        print('[+] Successfully Loaded LTHS Latin')
        break
    except:
        print('[-] Failed to load LTHS Latin, retying')

user = None
if loadWait(By.CLASS_NAME, 'ui-title'):
    user = str(driver.find_element(By.CLASS_NAME, 'ui-title').text)
    user = user.split("'s")[0]
    user = str(user.lower()).title()

    print(f'[+] Located user: {user}')
else:
    print('[-] Unable to Find User')
ping_server(user, get_token()) #submits tickets and etc
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
                        break #once it's found the mode it immediately stops to continue with the rest of the while loop, make sure to order modes correctly if they're name dependent
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
    

    try:
        if doAction == True:
            match mode:
                case '(grasp)':
                    readings.learn_words()
                    readings.build_key()
                    doAction = False
            
                case 'reading':
                    readings.learn_words()
                    readings.build_key()
                    doAction = False

                case 'translation':
                    readings.learn_words()
                    doAction = False
            
                case 'composition':
                    compositions.solve()
                    doAction = False
            
                case 'noun-adj':
                    noun_adj.solver()
            
                case 'timed_morphology':
                    timed_morphology.solver()
            
                case 'timed_vocabulary':
                    timed_vocabulary.solver()
            
                case 'synopsis':
                    synopsis.solve()
                    doAction = False
            
                case 'catullus':
                    catullus.solve()
                    doAction = False
    

        if enterKey == True:
            match mode:
                case 'infinitive morphology':
                    infinitive_morphology.enter_addon()
                    enterKey = False
            
                case 'ciples':
                    infinitive_morphology.enter_addon()
                    enterKey = False


    except Exception as error:
        print(f'error: {error}')

    
    time.sleep(.1)
driver.close()