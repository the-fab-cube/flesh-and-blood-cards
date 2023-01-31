import csv
import json
from pathlib import Path
from markdown_patch import unmark

def generate_json_file(language):
    print(f"Generating {language} keyword.json from keyword.csv...")

    keyword_array = []

    csvPath = Path(__file__).parent / f"../../../csvs/{language}/keyword.csv"
    jsonPath = Path(__file__).parent / f"../../../json/{language}/keyword.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            keyword_object = {}

            keyword_object['unique_id'] = row[0]
            keyword_object['name'] = row[1]
            keyword_object['description'] = row[2]
            keyword_object['description_plain'] = unmark(keyword_object['description'])

            keyword_array.append(keyword_object)

    json_object = json.dumps(keyword_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {language} keyword.json\n")