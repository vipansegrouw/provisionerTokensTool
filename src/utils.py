import csv
import json
from plistlib import Dict


def write_json_items_to_csv():
    items_list = []
    ids = []
    count = 0
    with open("resources/provisioner_token_items.json", 'r') as infile:
        json_dict: Dict = json.load(infile)
        for vendor, tabs in json_dict.items():
            for tab in tabs:
                for tab_name, items in tab.items():
                    for item in items:
                        id = item['id']
                        name = item['name']
                        count += 1
                        if id not in ids:
                            id_and_name = [id, name]
                            ids.append(id)
                            items_list.append(id_and_name)

    with open("resources/all_items.csv", 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(items_list)
