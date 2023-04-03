import csv
import json
from pathlib import Path

def generate_json_file(language):
    print(f"Generating {language} artist.json from artist.csv...")

    artist_array = []

    csvPath = Path(__file__).parent / f"../../../csvs/{language}/artist.csv"
    jsonPath = Path(__file__).parent / f"../../../json/{language}/artist.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')

        for row in reader:
            artist_object = {}

            artist_object['name'] = row['Name']

            artist_array.append(artist_object)

    json_object = json.dumps(artist_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {language} artist.json\n")