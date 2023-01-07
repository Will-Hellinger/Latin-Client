import json
import setup
import os

version = 0.1
user = 'none'

modes = ['synopsis', 'noun-adj', 'launchpad', '(grasp)', 'reading', 'composition', 'ciples', 'infinitive morphology', 'timed morphology']

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

try:
    try:
        actionButton = str(json.load(open('settings.json'))['configuration']['action-button'])
    except:
        actionButton = '`'
    
    webbrowserType = str(json.load(open('settings.json'))['configuration']['browser-type'])
    delay = int(json.load(open('settings.json'))['configuration']['timeout-delay'])

    discord_tracking = json.load(open('settings.json'))['configuration']['discord_tracking']
    discord_advertisement = json.load(open('settings.json'))['configuration']['discord_advertisement']
    discord_rpc = json.load(open('settings.json'))['configuration']['discord_rpc']

    funnySound = json.load(open('settings.json'))['configuration']['sound']

    latinLink = str(json.load(open('settings.json'))['schoology']['latin-link'])
    schoologyUser = str(json.load(open('settings.json'))['schoology']['username'])
    schoologyPass = str(json.load(open('settings.json'))['schoology']['password'])
    human_mode = json.load(open('settings.json'))['configuration']['fake-human']

    check_modified = [latinLink, schoologyPass, schoologyUser, webbrowserType]
    modified = True
    for a in range(len(check_modified)):
        if check_modified[a] == "none":
            modified = False
            setup.run()
    
    if modified == False:
        webbrowserType = str(json.load(open('settings.json'))['configuration']['browser-type'])
        latinLink = str(json.load(open('settings.json'))['schoology']['latin-link'])
        schoologyUser = str(json.load(open('settings.json'))['schoology']['username'])
        schoologyPass = str(json.load(open('settings.json'))['schoology']['password'])
except:
    setup.run()