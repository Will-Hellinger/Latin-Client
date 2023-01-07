import fnmatch, os, sys

if os.name == 'nt':
    subDirectory = '\\'
else:
    subDirectory = '/'

buildTypes = ['windows', 'mac', 'linux', 'website']
buildStructures = ['\\\\', '/', '/', '/']

if len(sys.argv) >= 2:
    if 'help' in str(sys.argv[1]):
        print('[data-mapper.py] [search directory] [output directory] [options: --ignore-windows --ignore-mac --ignore-linux --ignore-website]')
        sys.exit()

if len(sys.argv) >= 3:
    for a in range(len(sys.argv)):
        removeList = []
        for b in range(len(buildTypes)):
            if f'--ignore-{buildTypes[b]}' == sys.argv[a]:
                removeList.append(buildTypes[b])
        for b in range(len(removeList)):
            buildStructures.pop(buildTypes.index(removeList[b]))
            buildTypes.pop(buildTypes.index(removeList[b]))
    diradd1 = ''
    if str(sys.argv[1])[len(str(sys.argv[1]))-1] != subDirectory:
        diradd1 = subDirectory
    diradd2 = ''
    if str(sys.argv[2])[len(str(sys.argv[2]))-1] != subDirectory:
        diradd2 = subDirectory
    files = [os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(str(sys.argv[1])+diradd1)
        for f in fnmatch.filter(files, '*')]
    if os.path.exists(f'{str(sys.argv[2])+diradd2}structures') == False:
        os.mkdir(f'{str(sys.argv[2])+diradd2}structures')
    for a in range(len(buildTypes)):
        dataWrite = '{\n'
        for b in range(len(files)):
            if b != len(files) - 1:
                ending = ',\n'
            else:
                ending = '\n'
            dataWrite += f' "{(files[b].split(subDirectory)[len(files[b].split(subDirectory))-1])}": "{(files[b].replace(str(sys.argv[1])+diradd1, f".{subDirectory}")).replace(subDirectory, buildStructures[a])}"{ending}'
        dataWrite += '}'
        with open(f'{str(sys.argv[2])+diradd2}structures{subDirectory}{buildTypes[a]}-structure.json', 'w+') as f:
            f.write(dataWrite)