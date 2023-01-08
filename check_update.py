import requests
import hashlib
import os
import json
import sys

build_mode = False

#This is here to verify that this is not a github page lol
checksumFilename = 'chksm.json'
updateURL = 'https://will-hellinger.github.io/Latin-Client/'

if os.name == 'nt':
    subDirectory = '\\'
    pip = 'pip'
    clear = 'cls'
else:
    subDirectory = '/'
    pip = 'pip3'
    clear = 'clear'

def run():
    global checksumFilename
    doUpdate = True
    try:
        server_chksm = ((requests.get(f'{updateURL}main.chksm').content)).decode("utf-8").replace('\n', '')
        if 'repository' in server_chksm:
            doUpdate = False
    except:
        print('[-] Unable to check for updates')
        doUpdate = False
    
    
    if os.path.exists(checksumFilename):
        os.remove(checksumFilename)

    filelist = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            filelist.append(os.path.join(root,file))

    exclude_list = ['.pyc', '.DS_Store', 'settings.json', 'chksm.json', 'main.chksm']

    with open(checksumFilename, 'w') as temp_file:
        temp_file.write('{\n}')
    
    with open(checksumFilename, encoding='utf-8', mode='r+') as file:
        data = json.load(file)
        for name in filelist:
            useFile = True
            for a in range(len(exclude_list)):
                if name.endswith(exclude_list[a]) or '.git' in name: #dont want .git files to get tangled into/with mine
                    useFile = False
            if useFile == True:
                data[name.replace(subDirectory, "(sub)")] = hashlib.md5(open(name,'rb').read()).hexdigest()
#               print(f"{name} - {hashlib.md5(open(name,'rb').read()).hexdigest()}")
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    chksm = hashlib.md5(str(open(checksumFilename, encoding='utf-8', mode='r').read()).encode('utf-8')).hexdigest()
    data = json.load(open(checksumFilename, encoding='utf-8', mode='r'))

    with open('main.chksm', encoding='utf-8', mode='w') as file:
        file.write(str(chksm))

    if doUpdate == True:
        if chksm != server_chksm and build_mode == False:
            print(f'[-] Not up to date...\nCurrent Checksum: {chksm}\nServer Checksum: {server_chksm}\nDynamically updating...')
            newest_chksms = json.loads(requests.get(f'{updateURL}chksm.json').content)
            for item in newest_chksms:
                itemString = str(item)
                if (data.get(item) is None):
                    print(f'{itemString.replace("(sub)", subDirectory)}: Missing -> {newest_chksms[item]}')
                    try:
                        newData = (requests.get(f'{updateURL}{((itemString[1:]).replace("(sub)", "/"))[1:]}').content).decode('utf-8')
                        if "#This is here to verify that this is not a github page lol" in str(newData) or "The site configured at this address does not" not in str(newData):
                            with open(itemString.replace('(sub)', subDirectory), encoding='utf-8', mode='w') as file:
                                file.write(newData)
                        else:
                            print('maybe unable to find the file?')
                    except:
                        print('unable to download file, maybe its a server issue?')
                elif data[item] != newest_chksms[item]:
                    print(f'{itemString.replace("(sub)", subDirectory)}: {data[item]} -> {newest_chksms[item]}')
                    try:
                        newData = (requests.get(f'{updateURL}{((itemString[1:]).replace("(sub)", "/"))[1:]}').content).decode('utf-8')
                        if "#This is here to verify that this is not a github page lol" in str(newData) or "The site configured at this address does not" not in str(newData):
                            with open(itemString.replace('(sub)', subDirectory), encoding='utf-8', mode='w') as file:
                                file.write(newData)
                        else:
                            print('maybe unable to find the file?')
                    except:
                        print('unable to download file, maybe its a server issue?')

        else:
            if build_mode == False:
                print('[+] Up to date')
            else:
                print(f'[+] Building chksms: {server_chksm} -> {chksm}')
    elif build_mode == True:
        print(f'[+] Building chksms: Not connected -> {chksm}')

if len(sys.argv) >= 2:
    if str(sys.argv[1]) == 'build':
        build_mode = True
        run()