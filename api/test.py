import json


def count_unique_designs():
    dictionary = "./static/assets/data/3AD_dictionary_281.json"
    # dest = "../AccessLens-app/api/static/assets/data/3AD_dictionary_281_metadata_filled.json"

    with open(dictionary, 'r') as f:
        data = json.load(f)

    keys = list(data.keys())

    meta = list(data[keys[0]].keys())
    urls = []

    for k in keys:
        for m in meta:
            for d in data[k][m]:
                if d['design_url'] not in urls:
                    urls.append(d['design_url'])
                    
    print(len(urls))


def get_common_classes():
    dictionary = "./static/assets/data/3AD_dictionary.json"
    with open(dictionary, 'r') as f:
        data = json.load(f)

    keys = list(data.keys())
    IC_root_objects = ['handle', 'knob', 'electric outlet', 'faucet', 'button panel', 'switch']
    
    common_classes = []
    
    for key in keys:
        keyword = key.split("__")[0].strip().replace("_", " ")
        
        # custom 
        if keyword not in IC_root_objects and keyword not in common_classes:
            common_classes.append(keyword)
    
    
    return '. '.join(common_classes)

def main():
    print(get_common_classes())
    
    
if __name__ == "__main__":
    main()