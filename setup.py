import json
import validators
import os
import shutil


if os.name == 'nt':
    subdirectory = '\\'
    pip = 'pip'
    clear = 'cls'
else:
    subdirectory = '/'
    pip = 'pip3'
    clear = 'clear'

settings_path = f'.{subdirectory}data{subdirectory}settings.json'


def save_file(file: bytes, data: dict):
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()


def load_settings():
    if not os.path.exists(settings_path):
        shutil.copyfile(f'.{subdirectory}data{subdirectory}backup{subdirectory}base_settings.json', settings_path)
    with open(settings_path, 'r') as f:
        return json.load(f)


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


def run():
    try:
        settings = load_settings()
        with open(settings_path, 'w') as file:
        
            if settings['configuration']['browser-type'] == 'none':
                browser_type = get_browser_type()
                settings['configuration']['browser-type'] = browser_type
                save_file(file, settings)

            if settings['schoology']['latin-link'] == 'none':
                latin_link = get_latin_link()
                settings['schoology']['latin-link'] = latin_link
                save_file(file, settings)

            if settings['schoology']['username'] == 'none':
                creds = get_schoology_credentials()
                settings['schoology']['username'] = creds["username"]
                settings['schoology']['password'] = creds["password"]
                save_file(file, settings)

    except Exception as error:
        print(f'Error: {error}')
        exit()