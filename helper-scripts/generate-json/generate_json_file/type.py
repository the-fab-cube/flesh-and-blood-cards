import csv
import json
from pathlib import Path

def generate_json_file():
    print("Generating type.json from type.csv...")

    type_array = []

    csvPath = Path(__file__).parent / "../../../csvs/type.csv"
    jsonPath = Path(__file__).parent / "../../../json/type.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            type_object = {}

            type_object['name'] = row[0]

            type_array.append(type_object)

    json_object = json.dumps(type_array, indent=4)

    with jsonPath.open('w', newline='\n') as outfile:
        outfile.write(json_object)

    print("Successfully generated type.json\n")