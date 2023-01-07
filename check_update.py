import requests
from info import *
import hashlib
import os
import json

#This is here to verify that this is not a github page lol
checksumFilename = 'chksm.json'
updateURL = 'https://will-hellinger.github.io/Latin-Client/'

def run():
    global checksumFilename
    doUpdate = True
    try:
        server_chksm = ((requests.get(f'{updateURL}main.chksm').content)).decode("utf-8").replace('\n', '')
    except:
        print('[-] Unable to check for updates')
        doUpdate = False
    
    if doUpdate == True:
        if os.path.exists(checksumFilename):
            os.remove(checksumFilename)

        filelist = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                filelist.append(os.path.join(root,file))

        exclude_list = ['.pyc', '.DS_Store', 'settings.json']

        with open(checksumFilename, 'w') as temp_file:
            temp_file.write('{\n}')
    
        with open(checksumFilename, encoding='utf-8', mode='r+') as file:
            data = json.load(file)
            for name in filelist:
                useFile = True
                for a in range(len(exclude_list)):
                    if name.endswith(exclude_list[a]):
                        useFile = False
                if useFile == True:
                    data[name.replace(subDirectory, "(sub)")] = hashlib.md5(open(name,'rb').read()).hexdigest()
#                    print(f"{name} - {hashlib.md5(open(name,'rb').read()).hexdigest()}")
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

        chksm = hashlib.md5(str(open(checksumFilename, encoding='utf-8', mode='r').read()).encode('utf-8')).hexdigest()
        data = json.load(open(checksumFilename, encoding='utf-8', mode='r'))

        if chksm != server_chksm:
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
            print('[+] Up to date')
run()