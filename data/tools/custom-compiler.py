import os, sys, fnmatch, json
from pip._vendor import pkg_resources

if os.name == 'nt':
    subDirectory = '\\'
    seperator = ';'
    pip = 'pip'
else:
    subDirectory = '/'
    seperator = ':'
    pip = 'pip3'

if len(sys.argv) >= 2:
    removeModules = []
    neededModules = []
    modules = []
    splits = ['~', '>', '<', '+', '=', '[']
    if '.py' in str(sys.argv[1]):
        try:
            os.system(f'{pip} install pyinstaller')
            os.system(f'{pip} install pipreqs')
            print('\033[1;32;40m[+] Successfully installed compiling tools ')
        except:
            print(f'\033[1;31;40m[+] Failed to install compiling tools, continuing...\033[1;33;40m')
        if subDirectory not in str(sys.argv[1]):
            os.system(f'pipreqs --encoding utf-8 "{os.getcwd()}" --force')
            directory = os.getcwd() + subDirectory
        else:
            tempList = str(sys.argv[1]).split(subDirectory)
            directory = ''
            for a in range(len(tempList)-1):
                directory += tempList[a] + subDirectory
            os.system(f'pipreqs --encoding utf-8 "{directory[:-1]}" --force')
        if os.path.exists(f'{directory}needed_imports.txt'):
            os.remove(f'{directory}needed_imports.txt')
        os.rename(f'{directory}requirements.txt', f'{directory}needed_imports.txt')
        os.system(f'{pip} freeze > {directory}requirements.txt')
        with open(f'{directory}needed_imports.txt', 'r+') as f1:
            tempList = f1.read().split('\n')
            for a in range(len(tempList)-1):
                splitter = '='
                if ' @ ' in str(tempList[a]):
                    splitter = ' @ '
                neededModules.append(str(tempList[a]).split(splitter)[0])
                try:
                    _package = pkg_resources.working_set.by_key[str(tempList[a]).split(splitter)[0]]
                    for a in range(len([str(r) for r in _package.requires()])):
                        splitfound = False
                        for b in range(len(splits)):
                            if splitfound == False:
                                if splits[b] in str([str(r) for r in _package.requires()][a]).split(',')[0]:
                                    splitfound = True
                                    neededModules.append((str([str(r) for r in _package.requires()][a]).split(',')[0]).split(splits[b])[0])
                        if splitfound == False:
                            neededModules.append([str(r) for r in _package.requires()][a])
                except:
                    print(f'unable to load {str(tempList[a]).split(splitter)[0]} dependencies')
        extraModules = str(input('ExtraModules: ')).split(' ')
        for a in range(len(extraModules)):
            neededModules.append(extraModules[a])
        with open(f'{directory}requirements.txt', 'r+') as f2:
            tempList = f2.read().split('\n')
            for a in range(len(tempList)-1):
                splitter = '='
                if ' @ ' in str(tempList[a]):
                    splitter = ' @ '
                if str(tempList[a]).split(splitter)[0] not in neededModules:
                    removeModules.append(str(tempList[a]).split(splitter)[0])
        print(f'\033[1;32;40m[+] {len(neededModules)} modules needed')
        print(f'\033[1;32;40m[+] {len(removeModules)} modules removed')
        removeList = ''
        for a in range(len(removeModules)):
            removeList += f' --exclude-module {removeModules[a]} ^'
        settingsFile = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(directory)
            for f in fnmatch.filter(files, 'settings.json')]
        try:
            iconName = str(json.load(open(settingsFile[0]))['configuration']['icon'])
        except:
            iconName = 'icon.ico'
        icon = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(directory)
            for f in fnmatch.filter(files, iconName)]
        if len(icon) >= 1:
            os.system(f'pyinstaller --icon="{icon[0]}" "{str(sys.argv[1])}" --add-data="{directory}{seperator}." {str(removeList)}')
        else:
            os.system(f'pyinstaller "{str(sys.argv[1])}" --add-data="{directory}{seperator}." {str(removeList)}')
        input('[+] completed compilation')
sys.exit()