import json, validators
from system_commands import *
import shutil

if os.name == 'nt':
    subDirectory = '\\'
    pip = 'pip'
    clear = 'cls'
else:
    subDirectory = '/'
    pip = 'pip3'
    clear = 'clear'

def run():
    try:
        if not os.path.exists('settings.json'):
            shutil.copyfile(f'.{subDirectory}data{subDirectory}backup{subDirectory}base_settings.json', f'.{subDirectory}settings.json')
    
        if str(json.load(open('settings.json'))['configuration']['browser-type']) == "none":
            webbrowserTypes = ['Chrome', 'Chromium', 'Brave', 'Firefox', 'Internet Explorer', 'Edge', 'Opera']
            print('Browser Types:\n------------')
            for a in range(len(webbrowserTypes)):
                print(webbrowserTypes[a])
            print('------------')
            while True:
                webbrowserType = str(input('please enter your browser: '))
                if webbrowserType in webbrowserTypes:
                    break
                else:
                    print('please enter a valid browser type')
            with open('settings.json', 'r+') as f:
                data = json.load(f)
                data['configuration']['browser-type'] = webbrowserType
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
    
        if str(json.load(open('settings.json'))['schoology']['latin-link']) == "none":
            print('please enter the schoology link for the latin app')
            while True:
                latinLink = str(input('link: '))
                if validators.url(latinLink) == True:
                    break
                else:
                    print('invalid url')
            with open('settings.json', 'r+') as f:
                data = json.load(f)
                data['schoology']['latin-link'] = latinLink
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

        if str(json.load(open('settings.json'))['schoology']['username']) == "none":
            username = str(input('please enter schoology username: '))
            password = str(input('please enter schoology password: '))
            clear_console()
            with open('settings.json', 'r+') as f:
                data = json.load(f)
                data['schoology']['username'] = username
                data['schoology']['password'] = password
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
    except:
        print('error?')
        exit()