import json
import setup
import os

version = 1.0
user = 'none'

modes = ['synopsis', 'noun-adj', 'launchpad', '(grasp)', 'reading', 'composition', 'ciples', 'infinitive morphology', 'timed morphology', 'timed vocabulary']

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

try:
    try:
        actionButton = str(json.load(open(f'{path}settings.json'))['configuration']['action-button'])
    except:
        actionButton = '`'
    
    webbrowserType = str(json.load(open(f'{path}settings.json'))['configuration']['browser-type'])
    delay = int(json.load(open(f'{path}settings.json'))['configuration']['timeout-delay'])

    discord_rpc = json.load(open(f'{path}settings.json'))['configuration']['discord_rpc']

    funnySound = json.load(open(f'{path}settings.json'))['configuration']['sound']

    latinLink = str(json.load(open(f'{path}settings.json'))['schoology']['latin-link'])
    schoologyUser = str(json.load(open(f'{path}settings.json'))['schoology']['username'])
    schoologyPass = str(json.load(open(f'{path}settings.json'))['schoology']['password'])
    human_mode = json.load(open(f'{path}settings.json'))['configuration']['fake-human']

    check_modified = [latinLink, schoologyPass, schoologyUser, webbrowserType]
    modified = True
    for a in range(len(check_modified)):
        if check_modified[a] == "none":
            modified = False
            setup.run()
    
    if modified == False:
        webbrowserType = str(json.load(open(f'{path}settings.json'))['configuration']['browser-type'])
        latinLink = str(json.load(open(f'{path}settings.json'))['schoology']['latin-link'])
        schoologyUser = str(json.load(open(f'{path}settings.json'))['schoology']['username'])
        schoologyPass = str(json.load(open(f'{path}settings.json'))['schoology']['password'])
except:
    setup.run()