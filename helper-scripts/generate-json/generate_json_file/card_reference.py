import csv
import json
from pathlib import Path

def generate_json_file():
    print(f"Generating card-reference.json from card-reference.csv...")

    reference_array = []

    csvPath = Path(__file__).parent / f"../../../csvs/english/card-reference.csv"
    jsonPath = Path(__file__).parent / f"../../../json/english/card-reference.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            reference_object = {}

            reference_object['card_unique_id'] = row[0]
            reference_object['referenced_card_unique_id'] = row[3]

            reference_array.append(reference_object)

    json_object = json.dumps(reference_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated card-reference.json\n")