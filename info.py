import json
import os
import time
import random
import validators
import shutil
import glob
import requests
import unicodedata


try:
    import nltk
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    from nltk.corpus import wordnet
    nltk_usable = True
except:
    nltk_usable = False

version = 3.3
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


def clear_console() -> None:
    """
    Clear the console screen.

    :return: None
    """

    os.system(clear)


#great terminal commands
def get_file_count(directory: str) -> int:
    """
    Get the count of files in a directory.

    :param directory: The directory path.
    :return: The count of files as an integer.
    """

    directory = directory.replace('(sub)', subDirectory)

    if not directory.endswith(subDirectory):
        directory += subDirectory

    return len(glob.glob(f'{directory}*.*'))


def find_file(file_name: str, ignore_case: bool = False) -> list:
    """
    Find files with a given name in the current directory and its subdirectories.

    :param file_name: The name of the file to search for.
    :param ignore_case: Whether to perform a case-insensitive search.
    :return: A list of file paths that match the search criteria.
    """

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


def show_contents(file_name: str) -> None:
    """
    Display the contents of a file.

    :param file_name: The name of the file to display.
    :return: None
    """

    file_name = file_name.replace('(sub)', subDirectory)

    with open(file_name, mode='r', encoding='utf-8') as file:
        print(file.read())


def load_settings() -> None:
    """
    Load settings from a JSON file and update global variables accordingly.

    :return: None
    """

    global human_mode, discord_rpc, funnySound
    global latinLink, schoologyUser, schoologyPass, delay, webbrowserType, actionButton, tracking
    global compositions_fallback, timed_vocab_fallback, openai_enabled, openai_token, openai_model, compositions_synonyms_enabled, prediction_based_morphology, noun_adj_chart_name

    settings: dict = json.load(open(f'{path}settings.json', mode='r'))

    actionButton = settings['configuration'].get('action-button')
    if actionButton == None:
        actionButton = '`'

    webbrowserType = settings['configuration'].get('browser-type')
    delay = settings['configuration'].get('timeout-delay')
    human_mode = settings['configuration'].get('fake-human')
    noun_adj_chart_name = settings['configuration'].get('noun-adjective-chart')
    timed_vocab_fallback = settings['configuration'].get('google-trans-timed_vocab-fallback')
    compositions_fallback = settings['configuration'].get('google-trans-compositions-fallback')
    compositions_synonyms_enabled = settings['configuration'].get('synonyms-compositions-fallback') #do NOT recomend turning on, it helps improve points by little amounts and quadruples the inputs, but still an option
    prediction_based_morphology = settings['configuration'].get('prediction-based-morphology')

    openai_enabled = settings['configuration'].get('openai-catullus')
    openai_token = settings['open-ai'].get('token')
    openai_model = settings['open-ai'].get('model')

    discord_rpc = settings['configuration'].get('discord_rpc')
    funnySound = settings['configuration'].get('sound')
    tracking = settings['configuration'].get('tracking') #this is only really for diagnosing with multiple users orrrrr discord server integration (off by default)

    latinLink = settings['schoology'].get('latin-link')
    schoologyUser = settings['schoology'].get('username')
    schoologyPass = settings['schoology'].get('password')


def encode_file_name(file_name: str) -> str:
    """
    Encode a file name for safe storage by replacing special characters.

    :param file_name: The original file name.
    :return: The encoded file name as a string.
    """

    replace_dict: dict = {'\\': '(bs)', '?': '(qm)', '%': '(ps)', '*': '(a)', ':': '(c)', '|': '(p)', '"': '(qm)', '<': '(fa)', '>': '(ba)', ' ': '_'}

    for key, value in replace_dict.items():
        file_name = file_name.replace(key, value)
    
    file_name = file_name.encode('unicode-escape')
    file_name = file_name.decode('utf-8')
    file_name = file_name.replace('\\', '^')

    return file_name


def decode_file_name(file_name: str) -> str:
    """
    Decode a previously encoded file name.

    :param file_name: The encoded file name.
    :return: The decoded file name as a string.
    """

    replace_dict: dict = {'\\': '(bs)', '?': '(qm)', '%': '(ps)', '*': '(a)', ':': '(c)', '|': '(p)', '"': '(qm)', '<': '(fa)', '>': '(ba)', ' ': '_'}

    for key, value in replace_dict.items():
        file_name = file_name.replace(value, key)
    
    file_name = file_name.replace('^', '\\')
    file_name = file_name.encode('utf-8')
    file_name = file_name.decode('unicode-escape')

    return file_name


def save_file(file: bytes, data: dict) -> None:
    """
    Save data to a file.

    :param file: The file object.
    :param data: The data to save as a dictionary.
    :return: None
    """

    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()


def ping_server(user: str, token: str) -> None:
    """
    Ping the server with user information.

    :param user: The user's name.
    :param token: The user's token.
    :return: None
    """

    global server_url
    global tracking

    if tracking == True:
        try:
            requests.post(f'{server_url}/users', json={"name" : user, "token" : token})
        except:
            pass


def synonym_extractor(phrase: str) -> list:
    """
    Extract synonyms for a given phrase using NLTK WordNet.

    :param phrase: The phrase for which to find synonyms.
    :return: A list of synonyms as strings.
    """

    synonyms = []

    if nltk_usable == False:
        return None

    for syn in wordnet.synsets(phrase):
        for l in syn.lemmas():
            synonyms.append(l.name())

    return synonyms


def antonym_extractor(phrase: str) -> list:
    """
    Extract antonyms for a given phrase using NLTK WordNet.

    :param phrase: The phrase for which to find antonyms.
    :return: A list of antonyms as strings.
    """

    antonyms = []

    if nltk_usable == False:
        return None
    
    for syn in wordnet.synsets(phrase):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    
    return antonyms


def add_definition(word: str, meaning: str, location: str = 'latin_dictionary') -> None:
    """
    Add a definition for a word to a specific location.

    :param word: The word to add a definition for.
    :param meaning: The meaning or definition of the word.
    :param location: The location or dictionary to add the definition to.
    :return: None
    """

    word = word.replace('.json', '')
    file_path = f'.{subDirectory}data{subDirectory}{location}{subDirectory}{encode_file_name(word)}.json'

    if not os.path.exists(file_path):
        with open(file_path, mode='w', encoding='utf-8') as file:
            file.write('{\n}')
    
    with open(file_path, mode='r+', encoding='utf-8') as file:
        data = json.load(file)
        data[meaning] = True

        save_file(file, data)


def human_timeout(min: int = 1000, max: int = 5000) -> None:
    """
    Introduce a human-like timeout between actions.

    :param min: The minimum timeout duration in milliseconds.
    :param max: The maximum timeout duration in milliseconds.
    :return: None
    """
    
    global human_mode

    #min and max are in miliseconds

    if human_mode == True:
        time.sleep(int(random.randint(min, max))/1000)


def check_settings() -> dict:
    """
    Check and load settings from a JSON file, copying a backup if needed.

    :return: The loaded settings as a dictionary.
    """

    global subDirectory
    global path

    if not os.path.exists(f'{path}settings.json'):
        shutil.copyfile(f'.{subDirectory}data{subDirectory}backup{subDirectory}base_settings.json', f'{path}settings.json')
    
    try:
        return json.load(open(f'{path}settings.json', 'r'))
    except:
        shutil.copyfile(f'.{subDirectory}data{subDirectory}backup{subDirectory}base_settings.json', f'{path}settings.json')
    
    return json.load(open(f'{path}settings.json', 'r'))


def get_browser_type() -> str:
    """
    Prompt the user to select a browser type.

    :return: The selected browser type as a string.
    """

    while True:
        browser_types = ['Chrome', 'Chromium', 'Brave', 'Firefox', 'Internet Explorer', 'Edge', 'Opera']

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


def get_latin_link() -> str:
    """
    Prompt the user to enter the Schoology Latin app link.

    :return: The entered Latin app link as a string.
    """

    while True:
        link = input('Please enter the Schoology link for the Latin app: ')

        if validators.url(link) == True:
            return link
        else:
            print('Invalid URL, please try again.')


def get_schoology_credentials() -> dict:
    """
    Prompt the user to enter Schoology login credentials.

    :return: A dictionary containing the entered username and password.
    """

    username = input('Please enter your Schoology username: ')
    password = input('Please enter your Schoology password: ')

    return {"username" : username, "password" : password}


def setup() -> None:
    """
    Perform initial setup by prompting the user to enter missing settings.

    :return: None
    """

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


def spoof_activity(driver, type: str, response = None, aid = None) -> None:
    """
    Simulate activity on the web page, such as sending feedback.

    :param driver: The web driver object.
    :param type: The type of activity (e.g., 'translation' or 'grasp').
    :param response: The response for the activity.
    :param aid: The activity ID.
    :return: None
    """

    match type:
        case 'translation':
            cellID = 'translation_write'
            if aid is None:
                aid = '1100001016'
            if response is None:
                response = 'hi magistra'
            
            driver.execute_script('$.post("feedback.php", [{name:"why",value:"translation_score_initial"},{name:"aid",value:' + aid + '},{name:"cellID",value:' + cellID + '},{name:"response",value:' + response + '}],function(data){console.log(data)});')
        
        case 'grasp':
            score = '0'
            gid = '1'
            
            if aid is None:
                aid = '1100000001'
            if response is None:
                response = '"poet"'
            
            driver.execute_script('$.post("files/get_grasp_feedback.php", [{name:"aid", value:' + aid + '},{name:"score", value:' + score + '},{name:"gid", value:' + gid + '},{name:"response",value:' + response + '}], function(data){console.log(data)});')


def strip_accents(text: str) -> str:
    """
    Remove accents from a given text.

    :param text: The text to remove accents from.
    :return: The text without accents as a string.
    """

    return str(''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')).lower()


try:
    load_settings()

    if not os.path.exists(f'.{subDirectory}data{subDirectory}noun_adjective_dictionary{subDirectory}'):
        os.mkdir(f'.{subDirectory}data{subDirectory}noun_adjective_dictionary')

    if not os.path.exists(f'.{subDirectory}data{subDirectory}cache{subDirectory}'):
        os.mkdir(f'.{subDirectory}data{subDirectory}cache')

    settings_list = (webbrowserType, delay, human_mode, timed_vocab_fallback, compositions_fallback, discord_rpc, funnySound, latinLink, schoologyUser, schoologyPass)
    for setting in settings_list:
        if setting == None or setting == "none":
            setup()
    
    load_settings()

except:
    setup()
    load_settings()