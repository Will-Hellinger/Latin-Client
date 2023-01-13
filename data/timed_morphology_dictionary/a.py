import os
import json
filelist = []
converted_file_list = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if 'a.py' not in os.path.join(root,file) and 'key.json' not in os.path.join(root,file):
            filelist.append(os.path.join(root,file))
            converted_file_list.append(os.path.join(root,file))

removeList = ['\\', '?', '%', '*', ':', '|', '"', '<', '>']
replaceList = ['(bs)', '(qm)', '(ps)', '(a)', '(c)', '(p)', '(qm)', '(fa)', '(ba)']

if os.path.exists('key.json'):
    os.remove('key.json')

with open('key.json', 'w') as file:
    file.write('{\n}')

for a in range(len(converted_file_list)):

    converted_file_list[a] = str((str(converted_file_list[a]).encode('unicode-escape')).decode('utf-8')).replace("\\", "^")
    for b in range(len(removeList)):
        if removeList[b] in converted_file_list[a]:
            converted_file_list[a] = str(converted_file_list[a]).replace(str(removeList[b]), str(replaceList[b]))
            print(converted_file_list[a])
    with open('key.json', encoding='utf-8', mode='r+') as file:
        data = json.load(file)
        data[filelist[a].replace('./', '')] = converted_file_list[a].replace('./', '')
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    with open(filelist[a], encoding='unicode-escape', mode='r') as file:
        data = file.read()
    with open(converted_file_list[a], encoding='unicode-escape', mode='w') as file:
        data = data.split('\n')
        for b in range(len(data)):
            file.write(data[b])
            if b != len(data)-1:
                file.write('\n')
    os.remove(filelist[a])

    print(converted_file_list[a])