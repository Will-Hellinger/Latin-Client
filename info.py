import json
import setup
import os

version = 2.0
user = 'none'

modes = ['synopsis', 'noun-adj', 'launchpad', '(grasp)', 'reading', 'translation', 'composition', 'ciples', 'infinitive morphology', 'timed morphology', 'timed vocabulary']

doAction = False
enterKey = False

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

actionButton = "`"


def load_settings():
    global webbrowserType, delay, human_mode, timed_vocab_fallback, discord_rpc, funnySound, latinLink, schoologyUser, schoologyPass, actionButton
    settings = json.load(open(f'{path}settings.json', mode='r'))

    actionButton = settings['configuration'].get('action-button')
    if actionButton == None:
        actionButton = '`'

    webbrowserType = settings['configuration'].get('browser-type')
    delay = settings['configuration'].get('timeout-delay')
    human_mode = settings['configuration'].get('fake-human')
    timed_vocab_fallback = settings['configuration'].get('google-trans-timed_vocab-fallback')

    discord_rpc = settings['configuration'].get('discord_rpc')
    funnySound = settings['configuration'].get('sound')

    latinLink = settings['schoology'].get('latin-link')
    schoologyUser = settings['schoology'].get('username')
    schoologyPass = settings['schoology'].get('password')

try:
    load_settings()

    settings_list = (webbrowserType, delay, human_mode, timed_vocab_fallback, discord_rpc, funnySound, latinLink, schoologyUser, schoologyPass)
    for setting in settings_list:
        if setting == None or setting == "none":
            setup.run()
    
    load_settings()

except:
    setup.run()


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