import json
import os
import time
import random
import validators
import shutil
import glob

version = 3.0
user = 'none'

modes = ['synopsis', 'noun-adj', 'launchpad', '(grasp)', 'reading', 'catullus', 'translation', 'composition', 'ciples', 'infinitive morphology', 'timed morphology', 'timed vocabulary']

if os.name == 'nt':
    subDirectory = '\\'
    pip = 'pip'
    clear = 'cls'
else:
    subDirectory = '/'
    pip = 'pip3'
    clear = 'clear'

path = f'.{subDirectory}data{subDirectory}'


def clear_console():
    os.system(clear)

#great terminal commands
def get_file_count(directory: str):
    directory.replace('(sub)', subDirectory)

    if not directory.endswith(subDirectory):
        directory += subDirectory

    return len(glob.glob(f'{directory}*.*'))


def find_file(file_name: str, ignore_case = False):
    output = []

    for root, dirs, files in os.walk('.'):
        for file in files:
            
            if ignore_case == True:
                if file_name.lower() in file.lower() and '.git' not in root and '__pycache__' not in root:
                    output.append(os.path.join(root,file))
            
            else:
                if file_name in file and '.git' not in root and '__pycache__' not in root:
                    output.append(os.path.join(root,file))
    
    return output


def load_settings():
    global human_mode, discord_rpc, funnySound
    global latinLink, schoologyUser, schoologyPass, delay, webbrowserType, actionButton
    global compositions_fallback, timed_vocab_fallback, openai_enabled, openai_token, openai_model

    settings = json.load(open(f'{path}settings.json', mode='r'))

    actionButton = settings['configuration'].get('action-button')
    if actionButton == None:
        actionButton = '`'

    webbrowserType = settings['configuration'].get('browser-type')
    delay = settings['configuration'].get('timeout-delay')
    human_mode = settings['configuration'].get('fake-human')
    timed_vocab_fallback = settings['configuration'].get('google-trans-timed_vocab-fallback')
    compositions_fallback = settings['configuration'].get('google-trans-compositions-fallback')

    openai_enabled = settings['configuration'].get('')
    openai_token = settings['open-ai'].get('token')
    openai_model = settings['open-ai'].get('model')

    discord_rpc = settings['configuration'].get('discord_rpc')
    funnySound = settings['configuration'].get('sound')

    latinLink = settings['schoology'].get('latin-link')
    schoologyUser = settings['schoology'].get('username')
    schoologyPass = settings['schoology'].get('password')


def encodeFilename(file_name: str):
    removeList = ['\\', '?', '%', '*', ':', '|', '"', '<', '>', ' ']
    replaceList = ['(bs)', '(qm)', '(ps)', '(a)', '(c)', '(p)', '(qm)', '(fa)', '(ba)', '_']
    for a in range(len(removeList)):
        file_name = file_name.replace(str(removeList[a]), str(replaceList[a]))
    
    file_name = file_name.encode('unicode-escape')
    file_name = file_name.decode('utf-8')
    file_name = file_name.replace('\\', '^')

    return file_name


def decodeFilename(file_name: str):
    removeList = ['\\', '?', '%', '*', ':', '|', '"', '<', '>', ' ']
    replaceList = ['(bs)', '(qm)', '(ps)', '(a)', '(c)', '(p)', '(qm)', '(fa)', '(ba)', '_']
    for a in range(len(removeList)):
        file_name = file_name.replace(str(replaceList[a]), str(removeList[a]))
    
    file_name = file_name.replace('^', '\\')
    file_name = file_name.encode('utf-8')
    file_name = file_name.decode('unicode-escape')

    return file_name


def save_file(file: bytes, data: dict):
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()


def human_timeout(min = 1000, max = 5000):
    global human_mode

    #min and max are in miliseconds

    if human_mode == True:
        time.sleep(int(random.randint(min, max))/1000)


def check_settings():
    if not os.path.exists(f'{path}settings.json'):
        shutil.copyfile(f'.{subDirectory}data{subDirectory}backup{subDirectory}base_settings.json', f'{path}settings.json')
    
    try:
        return json.load(open(f'{path}settings.json', 'r'))
    except:
        shutil.copyfile(f'.{subDirectory}data{subDirectory}backup{subDirectory}base_settings.json', f'{path}settings.json')
    
    return json.load(open(f'{path}settings.json', 'r'))


def get_browser_type():
    while True:
        browser_types = ['Chrome', 'Chromium', 'Brave', 'Firefox', 'Internet Explorer', 'Edge', 'Opera', 'Safari']

        print('Browser Types:\n------------')
        for a, browser_type in enumerate(browser_types):
            print(f'{a + 1}. {browser_type}')
        print('------------')

        choice = input('Please enter the number of your browser: ')

        try:
            index = int(choice) - 1
            if index >= 0 and index < len(browser_types):
                return browser_types[index]
        except:
            pass

        print('Invalid choice, please try again.')


def get_latin_link():
    while True:
        link = input('Please enter the Schoology link for the Latin app: ')

        if validators.url(link) == True:
            return link
        else:
            print('Invalid URL, please try again.')


def get_schoology_credentials():
    username = input('Please enter your Schoology username: ')
    password = input('Please enter your Schoology password: ')

    return {"username" : username, "password" : password}


def setup():
    try:
        settings = check_settings()
        with open(f'{path}settings.json', 'r+') as file:
        
            if settings['configuration']['browser-type'] == 'none':
                browser_type = get_browser_type()
                settings['configuration']['browser-type'] = browser_type

            if settings['schoology']['latin-link'] == 'none':
                latin_link = get_latin_link()
                settings['schoology']['latin-link'] = latin_link

            if settings['schoology']['username'] == 'none':
                creds = get_schoology_credentials()
                settings['schoology']['username'] = creds["username"]
                settings['schoology']['password'] = creds["password"]
            
            save_file(file, settings)

    except Exception as error:
        print(f'Error: {error}')
        exit()



try:
    load_settings()

    settings_list = (webbrowserType, delay, human_mode, timed_vocab_fallback, compositions_fallback, discord_rpc, funnySound, latinLink, schoologyUser, schoologyPass)
    for setting in settings_list:
        if setting == None or setting == "none":
            setup()
    
    load_settings()

except:
    setup()