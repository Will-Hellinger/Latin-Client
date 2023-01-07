from asyncore import write
import json, os, glob

if not os.path.exists('./output.json'):
    with open(f"./output.json", encoding='utf-8', mode='w') as write_file:
        write_file.write('{\n}')

with open(f"./output.json", encoding='utf-8', mode='r+') as data_file: 
    data = json.load(data_file)
    for file in glob.glob("*.json"):
        with open(f"./{file}", encoding='utf-8') as temp_file:                           
            temp_data = json.load(temp_file)
            for item in temp_data:
                data[(file.split('.json')[0] + " - " + item)] = temp_data[item]
                print((file.split('.json')[0] + " - " + item) + ' = ' + str(temp_data[item]))
    data_file.seek(0)
    json.dump(data, data_file, indent=4)
    data_file.truncate()