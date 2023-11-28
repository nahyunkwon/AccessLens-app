import json

dictionary = "./static/assets/data/3AD_dictionary_281.json"
# dest = "../AccessLens-app/api/static/assets/data/3AD_dictionary_281_metadata_filled.json"

with open(dictionary, 'r') as f:
    data = json.load(f)

keys = list(data.keys())

meta = list(data[keys[0]].keys())

count = 0

for k in keys:
    print(k)