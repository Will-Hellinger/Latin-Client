import json

with open("./data/noun-adj_chart.json", encoding='utf-8') as file:
    data = json.load(file)
    allEndings = []
    for item in data:
        allEndings.append([item, data[item]])
    
print(allEndings)