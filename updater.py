import requests
import hashlib
import os
import json
import sys

#This is here to verify that this is not a github page lol

if os.name == 'nt':
    subDirectory = '\\'
    pip = 'pip'
    clear = 'cls'
else:
    subDirectory = '/'
    pip = 'pip3'
    clear = 'clear'

path = f'.{subDirectory}data{subDirectory}'
checksum_filename = 'chksm.json'
main_checksum_filename = 'main.chksm'
updateURL = 'https://will-hellinger.github.io/Latin-Client/'
checksumURL = f'{updateURL}{str(str(path[1:]).replace(subDirectory, "/")[1:])}'
exclude_list = ['.pyc', '.DS_Store', 'settings.json', checksum_filename, main_checksum_filename, '.git']
user_updated_folders = ['latin_dictionary', 'timed_morphology_dictionary', 'timed_vocab_dictionary']
settings_file_dir = f'.{subDirectory}data{subDirectory}'
backup_settings_dir = f'.{subDirectory}data{subDirectory}backup{subDirectory}'
settings_file_name = 'settings.json'
backup_settings_name = 'base_settings.json'

build_commands = ['-b', '--b', '-build', '--build']
run_commands = ['-r', '--r', '-run', '--run']
check_update_commands = ['-c', '--c', '-check', '--check']

def check_valid_url(text: str):
    if "#This is here to verify that this is not a github page lol" in text or "The site configured at this address does not" not in text:
        return True
    
    return False


def save_file(file: bytes, data: dict):
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()


def create_chksms(print_filenames: bool = False):
    global path
    global checksum_filename
    global updateURL
    global exclude_list
    global checksumURL

    if os.path.exists(f'{path}{checksum_filename}'):
        os.remove(f'{path}{checksum_filename}')
    if os.path.exists(f'{path}{main_checksum_filename}'):
        os.remove(f'{path}{main_checksum_filename}')
    
    filelist = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            filelist.append(os.path.join(root,file))

    with open(f'{path}{checksum_filename}', 'w') as temp_file:
        temp_file.write('{\n}')
    
    with open(f'{path}{checksum_filename}', encoding='utf-8', mode='r+') as file:
        data = json.load(file)
        for name in filelist:
            useFile = True

            for a in range(len(exclude_list)):
                if name.endswith(exclude_list[a]) or '.git' in name:
                    useFile = False
                    break

            if useFile == True:
                if print_filenames == True:
                    print(f'{name}\t\t', end='\r')
                hash = hashlib.md5(open(name,'rb').read()).hexdigest()
                data[name.replace(subDirectory, "(sub)")] = hash
        save_file(file, data)

    chksm = hashlib.md5(str(open(f'{path}{checksum_filename}', encoding='utf-8', mode='r').read()).encode('utf-8')).hexdigest()
    with open(f'{path}{main_checksum_filename}', encoding='utf-8', mode='w') as file:
        file.write(str(chksm))


def check_update():
    global path
    global checksum_filename
    global updateURL
    global exclude_list
    global checksumURL

    try:
        server_chksm = ((requests.get(f'{checksumURL}{main_checksum_filename}').content)).decode("utf-8").replace('\n', '')
        if 'repository' in server_chksm or "The site configured at this address does not" in server_chksm:
            return False
    except:
        return False

    create_chksms()
    chksm = open(f'{path}{main_checksum_filename}', mode='r').read()
    
    if chksm != server_chksm:
        return True

    return False


def update():
    global path
    global checksum_filename
    global updateURL
    global exclude_list
    global checksumURL
    global user_updated_folders

    chksm = open(f'{path}{main_checksum_filename}', mode='r').read()

    try:
        server_chksm = ((requests.get(f'{checksumURL}{main_checksum_filename}').content)).decode("utf-8").replace('\n', '')
        if 'repository' in server_chksm or "The site configured at this address does not" in server_chksm:
            return False
    except:
        return False
    
    server_chksms = json.loads(requests.get(f'{checksumURL}chksm.json').content)
    data = json.load(open(f'{path}{checksum_filename}', encoding='utf-8', mode='r'))

    print(f'[-] Not up to date...\nCurrent Checksum: {chksm}\nServer Checksum: {server_chksm}\nDynamically updating...')

    for item in server_chksms:
        print(f'scanning: {str(item)}', end='\r')
        if data.get(item) != None and ('latin_dictionary' in str(item) or 'timed_morphology_dictionary' in str(item) or 'timed_vocab_dictionary' in str(item)):
            break

        if (data.get(item) != server_chksms[item]):
            print(f'{str(item).replace("(sub)", subDirectory)}: {data[item]} -> {server_chksms[item]}')

            newData = (requests.get(f'{updateURL}{((str(item)[1:]).replace("(sub)", "/"))[1:]}').content).decode('utf-8')
            user_updatable_file = False

            if check_valid_url(newData) == False:
                pass

            for a in range(len(user_updated_folders)):
                if user_updated_folders[a] in str(item):
                    user_updated_file = True

            if os.path.exists(item.replace("(sub)", subDirectory)) and user_updatable_file == True:
                temp_file = open(item.replace("(sub)", subDirectory), encoding='utf-8', mode='r+')
                temp_server_data = json.loads(newData)
                temp_client_data = json.load(temp_file)

                for item in temp_client_data:
                    if temp_client_data.get(item) == None:
                        temp_client_data[item] = temp_server_data[item]
                save_file(temp_file, temp_client_data)
            
            elif (os.path.exists(item.replace("(sub)", subDirectory)) and user_updatable_file == False) or not os.path.exists(item.replace("(sub)", subDirectory)):
                with open(str(item).replace('(sub)', subDirectory), encoding='utf-8', mode='w') as file:
                    file.write(newData)
    
    #allows for settings to be updated as well
    base_settings = json.load(open(f'{backup_settings_dir}{backup_settings_name}', mode='r'))
    with open(f'{settings_file_dir}{settings_file_name}', mode='r+') as file:
        settings = json.load(file)

        for item in base_settings:
            if settings.get(item) == None:
                settings[item] = base_settings[item]
    
    save_file(file, settings)


def build_chksm():
    global path
    global checksum_filename
    global updateURL
    global exclude_list
    global checksumURL

    create_chksms()

    try:
        server_chksm = ((requests.get(f'{checksumURL}{main_checksum_filename}').content)).decode("utf-8").replace('\n', '')
        if 'repository' in server_chksm or "The site configured at this address does not" in server_chksm:
            server_chksm = 'unavailable'
    except:
        server_chksm = 'unavailable'
    
    chksm = open(f'{path}{main_checksum_filename}', mode='r').read()
    
    print(f'[+] Building chksms: {server_chksm} -> {chksm}')


if len(sys.argv) >= 2:
    if str(sys.argv[1]) in build_commands:
        build_chksm()
    elif str(sys.argv[1]) in run_commands:
        if check_update() == True:
            update()
    elif str(sys.argv[1]) in check_update_commands:
        if check_update() == True:
            print('Update found!')
        else:
            print('No updates found')