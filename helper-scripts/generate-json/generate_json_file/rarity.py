import csv
import json
from pathlib import Path

def generate_json_file():
    print("Generating rarity.json from rarity.csv...")

    rarity_array = []

    csvPath = Path(__file__).parent / "../../../csvs/english/rarity.csv"
    jsonPath = Path(__file__).parent / "../../../json/english/rarity.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            rarity_object = {}

            rarity_object['id'] = row[0]
            rarity_object['description'] = row[1]

            rarity_array.append(rarity_object)

    json_object = json.dumps(rarity_array, indent=4)

    with jsonPath.open('w', newline='\n') as outfile:
        outfile.write(json_object)

    print("Successfully generated rarity.json\n")