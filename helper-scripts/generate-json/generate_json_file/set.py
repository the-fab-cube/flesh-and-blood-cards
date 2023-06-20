import csv
import json
import re
from pathlib import Path

import convert_set_printings_to_dict

def generate_json_file(language):
    print(f"Generating {language} set.json from set.csv...")

    set_array = []

    set_csv_path = Path(__file__).parent / f"../../../csvs/english/set.csv"
    set_printing_csv_path = Path(__file__).parent / f"../../../csvs/{language}/set-printing.csv"

    set_json_path = Path(__file__).parent / f"../../../json/{language}/set.json"

    set_printing_dict = convert_set_printings_to_dict.convert_set_printings_to_dict(set_printing_csv_path)

    with set_csv_path.open(newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')

        for row in reader:
            set_unique_id = row['Unique ID']

            if set_unique_id not in set_printing_dict:
                continue

            set_object = {}

            set_object['unique_id'] = set_unique_id
            set_object['id'] = row['Identifier']
            set_object['name'] = row['Name']

            # Set Printings

            set_printing_array = set_printing_dict[set_unique_id]

            set_object['printings'] = set_printing_array

            set_array.append(set_object)

    json_object = json.dumps(set_array, indent=4, ensure_ascii=False)

    with set_json_path.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {language} set.json\n")