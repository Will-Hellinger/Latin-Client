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

def save_file(file: bytes, data: dict):
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()

def run():
    global checksumFilename
    global updateURL
    doUpdate = True
    exclude_list = ['.pyc', '.DS_Store', 'settings.json', 'chksm.json', 'main.chksm', '.git']
    
    try:
        server_chksm = ((requests.get(f'{updateURL}main.chksm').content)).decode("utf-8").replace('\n', '')
        if 'repository' in server_chksm or "The site configured at this address does not" in server_chksm:
            doUpdate = False
    except:
        print('[-] Unable to check for updates')
        doUpdate = False

    if doUpdate == False:
        exit

    if os.path.exists(checksumFilename):
        os.remove(checksumFilename)
    filelist = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            filelist.append(os.path.join(root,file))

    with open(checksumFilename, 'w') as temp_file:
        temp_file.write('{\n}')
    
    with open(checksumFilename, encoding='utf-8', mode='r+') as file:
        data = json.load(file)
        for name in filelist:
            useFile = True
            for a in range(len(exclude_list)):
                if name.endswith(exclude_list[a]) or '.git' in name:
                    useFile = False
            if useFile == True:
                hash = hashlib.md5(open(name,'rb').read()).hexdigest()
                data[name.replace(subDirectory, "(sub)")] = hash
                if build_mode == True:
                    print(f"{name} - {hash}", end='\r')
        save_file(file, data)

    chksm = hashlib.md5(str(open(checksumFilename, encoding='utf-8', mode='r').read()).encode('utf-8')).hexdigest()
    data = json.load(open(checksumFilename, encoding='utf-8', mode='r'))
    with open('main.chksm', encoding='utf-8', mode='w') as file:
        file.write(str(chksm))
    
    if chksm != server_chksm and build_mode == False:
        print(f'[-] Not up to date...\nCurrent Checksum: {chksm}\nServer Checksum: {server_chksm}\nDynamically updating...')
        newest_chksms = json.loads(requests.get(f'{updateURL}chksm.json').content)
        for item in newest_chksms:
            print(f'scanning: {str(item)}', end='\r')

            if (data.get(item) != newest_chksms[item]):
                print(f'{str(item).replace("(sub)", subDirectory)}: {data[item]} -> {newest_chksms[item]}')

                newData = (requests.get(f'{updateURL}{((str(item)[1:]).replace("(sub)", "/"))[1:]}').content).decode('utf-8')
                if "#This is here to verify that this is not a github page lol" in str(newData) or "The site configured at this address does not" not in str(newData):
                    with open(str(item).replace('(sub)', subDirectory), encoding='utf-8', mode='w') as file:
                        file.write(newData)

    elif chksm == server_chksm and build_mode == False:
        print(f'[+] Up to Date')

    elif build_mode == True:
        if doUpdate == False:
            server_chksm = 'Not Connected'
        
        print(f'[+] Building chksms: {server_chksm} -> {chksm}')

if len(sys.argv) >= 2:
    if str(sys.argv[1]) == 'build':
        build_mode = True
        run()
    elif str(sys.argv[1]) == 'run':
        run()