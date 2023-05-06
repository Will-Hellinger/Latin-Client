import json
import os
import time
import random
import validators
import shutil
import glob
import requests

try:
    import nltk
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    from nltk.corpus import wordnet

    nltk_usable = True
except:
    nltk_usable = False

version = 3.0
user = 'none'
server_url = 'http://localhost:3000'

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
    directory = directory.replace('(sub)', subDirectory)

    if not directory.endswith(subDirectory):
        directory += subDirectory

    return len(glob.glob(f'{directory}*.*'))


def find_file(file_name: str, ignore_case = False):
    output = []

    for root, dirs, files in os.walk('.'):
        for file in files:

            if '.git' in root or '__pycache__' in root:
                continue

            file_original_name = file
            
            if ignore_case == True:
                file_name = file_name.lower()
                file = file.lower()

            if file_name in file:
                output.append(os.path.join(root, file_original_name))
    
    return output


def show_contents(file_name: str):
    file_name = file_name.replace('(sub)', subDirectory)

    with open(file_name, mode='r', encoding='utf-8') as file:
        print(file.read())


def load_settings():
    global human_mode, discord_rpc, funnySound
    global latinLink, schoologyUser, schoologyPass, delay, webbrowserType, actionButton, tracking
    global compositions_fallback, timed_vocab_fallback, openai_enabled, openai_token, openai_model, compositions_synonyms_enabled

    settings = json.load(open(f'{path}settings.json', mode='r'))

    actionButton = settings['configuration'].get('action-button')
    if actionButton == None:
        actionButton = '`'

    webbrowserType = settings['configuration'].get('browser-type')
    delay = settings['configuration'].get('timeout-delay')
    human_mode = settings['configuration'].get('fake-human')
    timed_vocab_fallback = settings['configuration'].get('google-trans-timed_vocab-fallback')
    compositions_fallback = settings['configuration'].get('google-trans-compositions-fallback')
    compositions_synonyms_enabled = settings['configuration'].get('synonyms-compositions-fallback') #do NOT recomend turning on, it helps improve points by little amounts and quadruples the inputs, but still an option

    openai_enabled = settings['configuration'].get('')
    openai_token = settings['open-ai'].get('token')
    openai_model = settings['open-ai'].get('model')

    discord_rpc = settings['configuration'].get('discord_rpc')
    funnySound = settings['configuration'].get('sound')
    tracking = settings['configuration'].get('tracking') #this is only really for diagnosing with multiple users orrrrr discord server integration (off by default)

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


def ping_server(user: str, token: str):
    global server_url
    global tracking

    if tracking == True:
        try:
            requests.post(f'{server_url}/users', json={"name" : user, "token" : token})
        except:
            pass


def synonym_extractor(phrase: str):
    synonyms = []

    if nltk_usable == False:
        return None

    for syn in wordnet.synsets(phrase):
        for l in syn.lemmas():
            synonyms.append(l.name())

    return synonyms


def antonym_extractor(phrase: str):
    antonyms = []

    if nltk_usable == False:
        return None
    
    for syn in wordnet.synsets(phrase):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    
    return antonyms


def human_timeout(min = 1000, max = 5000):
    global human_mode

    #min and max are in miliseconds

    if human_mode == True:
        time.sleep(int(random.randint(min, max))/1000)


def check_settings():
    global subDirectory
    global path

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

    if not os.path.exists(f'.{subDirectory}data{subDirectory}cache{subDirectory}'):
        os.mkdir(f'.{subDirectory}data{subDirectory}cache')

    settings_list = (webbrowserType, delay, human_mode, timed_vocab_fallback, compositions_fallback, discord_rpc, funnySound, latinLink, schoologyUser, schoologyPass)
    for setting in settings_list:
        if setting == None or setting == "none":
            setup()
    
    load_settings()

except:
    setup()