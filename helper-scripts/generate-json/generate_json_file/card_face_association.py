import csv
import json
from pathlib import Path

def generate_json_file(language):
    print(f"Generating {language} card-face-association.json from card-face-association.csv...")

    association_array = []

    csvPath = Path(__file__).parent / f"../../../csvs/{language}/card-face-association.csv"
    jsonPath = Path(__file__).parent / f"../../../json/{language}/card-face-association.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            association_object = {}

            association_object['front_unique_id'] = row[0]
            association_object['back_unique_id'] = row[3]
            association_object['is_DFC'] = True if row[6] == "Yes" else False if row[6] == "No" else None

            association_array.append(association_object)

    json_object = json.dumps(association_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {language} card-face-association.json\n")