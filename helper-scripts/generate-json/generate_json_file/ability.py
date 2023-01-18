import csv
import json
from pathlib import Path

def generate_json_file(language):
    print(f"Generating {language} ability.json from ability.csv...")

    ability_array = []

    csvPath = Path(__file__).parent / f"../../../csvs/{language}/ability.csv"
    jsonPath = Path(__file__).parent / f"../../../json/{language}/ability.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            ability_object = {}

            ability_object['unique_id'] = row[0]
            ability_object['name'] = row[1]

            ability_array.append(ability_object)

    json_object = json.dumps(ability_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully {language} generated ability.json\n")