import json, os
if os.name == 'nt':
    subDirectory = '\\'
else:
    subDirectory = '/'

with open(f".{subDirectory}data{subDirectory}backup{subDirectory}timed_dictionary.json", encoding='utf-8') as data_file:                           
    data = json.load(data_file)


for item in data:
    print(item.split(' - ')[0])
#    word = ((((str(item.split(" - ")[0])).encode('unicode-escape')).decode('utf-8')).replace('\\', '')).replace(' ', '_')
    word = str(item.split(" - ")[0]).replace(' ', '_')
    if os.path.exists(f'.{subDirectory}data{subDirectory}timed_dictionary{subDirectory}{word}.json') == False:
        temp_file = open(f'.{subDirectory}data{subDirectory}timed_dictionary{subDirectory}{word}.json', 'w')
        temp_file.write('{\n}')
        temp_file.close()

    with open(f'.{subDirectory}data{subDirectory}timed_dictionary{subDirectory}{word}.json', encoding='utf-8', mode='r+') as file:
        dict_data = json.load(file)
        dict_data[item.split(' - ')[1]] = data[item]
        file.seek(0)
        json.dump(dict_data, file, indent=4)
        file.truncate()