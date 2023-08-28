import pandas as pd
import json


def thingiverse_designs(design_csv):
    """
    Create thingiverse design information json 
    """
    designs = pd.read_csv(design_csv)

    designs_dict = {}
    
    for i in range(len(designs)):
        thing_id = int(designs.iloc[i]['id'])
    
        url = designs.iloc[i]['url']
        image_url = designs.iloc[i]['image']
        # try:
        #     name = designs.iloc[i]['name'].replace('\'', '')
        # except:
        #     print(designs.iloc[i]['name'])
        tags = designs.iloc[i]['tags']

        designs_dict[thing_id] = {}
        designs_dict[thing_id]['design_url'] = url if type(url) == str else ""
        designs_dict[thing_id]['image_url'] = image_url if type(image_url) == str else ""
        # designs_dict[thing_id]['title'] = name if type(name) == str else ""
        designs_dict[thing_id]['tags'] = tags if type(tags) == str else ""

    with open('./3AD_design_info.json', 'w') as f:
        json.dump(designs_dict, f)


def design_to_dict(design_csv):
    """
    Convert design csv file with manual annotation to dictionary format to be used in application
    CSV file has thingiverse url, thumbnail image, and annotations
    IC: inaccessibility class
    AccessMeta: assistive design categories
    """

    designs = pd.read_csv(design_csv)

    designs_dict = {}

    accessmeta = ['actuation-operation',
                  'actuation-reach',
                  'constraint',
                  'indication-visual',
                  'indication-tactile']
    
    # parsing designs with object & accessmeta categories
    
    for i in range(len(designs)):
        ic = designs.iloc[i]['IC']
        
        if type(ic) == str:
            category = designs.iloc[i]['AccessMeta']

            ics = [x.strip() for x in ic.split(',')]
            categories = [x.strip() for x in category.split(',')]

            url = designs.iloc[i]['url']
            thing_id = str(int(designs.iloc[i]['id']))

            for obj in ics:
                # remove number id from accessdb classes
                obj = obj.split(" ")[-1]

                if obj not in list(designs_dict.keys()):
                    designs_dict[obj] = {}
                    for meta in accessmeta:
                        designs_dict[obj][meta] = []
                
                for cat in categories:
                    designs_dict[obj][cat].append(url)


    with open('./3AD_dictionary.json', 'w') as f:
        json.dump(designs_dict, f)
    

        # if ',' in ic:
        #     ics = [x.strip() for x in ic.split(',')]
            
        # else:
        #     ics = [ic.strip()]

        # for c in ics:
        #     designs_dict[c].append()
        

        


def main():
    design_csv = './assistive_design_dict.csv'
    thingiverse_designs(design_csv)
    # design_to_dict(design_csv)

if __name__ == "__main__":
    main()