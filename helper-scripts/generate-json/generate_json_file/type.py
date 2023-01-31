import csv
import json
from pathlib import Path

def generate_json_file(language):
    print(f"Generating {language} type.json from type.csv...")

    type_array = []

    csvPath = Path(__file__).parent / f"../../../csvs/{language}/type.csv"
    jsonPath = Path(__file__).parent / f"../../../json/{language}/type.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            type_object = {}

            type_object['unique_id'] = row[0]
            type_object['name'] = row[1]

            type_array.append(type_object)

    json_object = json.dumps(type_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully {language} generated type.json\n")