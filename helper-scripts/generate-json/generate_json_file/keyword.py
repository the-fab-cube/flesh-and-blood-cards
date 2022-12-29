import csv
import json
from pathlib import Path
from markdown_patch import unmark

def generate_json_file():
    print("Generating keyword.json from keyword.csv...")

    keyword_array = []

    csvPath = Path(__file__).parent / "../../../csvs/english/keyword.csv"
    jsonPath = Path(__file__).parent / "../../../json/english/keyword.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            keyword_object = {}

            keyword_object['keyword'] = row[0]
            keyword_object['description'] = row[1]
            keyword_object['description_plain'] = unmark(keyword_object['description'])

            keyword_array.append(keyword_object)

    json_object = json.dumps(keyword_array, indent=4)

    with jsonPath.open('w', newline='\n') as outfile:
        outfile.write(json_object)

    print("Successfully generated keyword.json\n")