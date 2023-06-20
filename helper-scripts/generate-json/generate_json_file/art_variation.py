import csv
import json
from pathlib import Path

def generate_json_file():
    print("Generating art-variation.json from art-variation.csv...")

    art_variation_array = []

    csvPath = Path(__file__).parent / "../../../csvs/english/art-variation.csv"
    jsonPath = Path(__file__).parent / "../../../json/english/art-variation.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            art_variation_object = {}

            art_variation_object['id'] = row[0]
            art_variation_object['name'] = row[1]

            art_variation_array.append(art_variation_object)

    json_object = json.dumps(art_variation_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print("Successfully generated art-variation.json\n")