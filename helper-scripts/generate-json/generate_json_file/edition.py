import csv
import json
from pathlib import Path

def generate_json_file():
    print("Generating edition.json from edition.csv...")

    edition_array = []

    csvPath = Path(__file__).parent / "../../../csvs/english/edition.csv"
    jsonPath = Path(__file__).parent / "../../../json/english/edition.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            edition_object = {}

            edition_object['id'] = row[0]
            edition_object['name'] = row[1]

            edition_array.append(edition_object)

    json_object = json.dumps(edition_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print("Successfully generated edition.json\n")