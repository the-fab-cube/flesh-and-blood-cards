import csv
import json
from pathlib import Path

def generate_json_file(filename):
    print(f"Generating {filename}.json from {filename}.csv...")

    legality_array = []

    csvPath = Path(__file__).parent / f"../../../csvs/english/{filename}.csv"
    jsonPath = Path(__file__).parent / f"../../../json/english/{filename}.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')

        for row in reader:
            legality_object = {}

            legality_object['unique_id'] = row['Unique ID']

            legality_object['card_unique_id'] = row['Card Unique ID']

            status_active = True if row['Status Active'] == "Yes" else False if row['Status Active'] == "No" else None
            legality_object['status_active'] = status_active

            if 'Affects Full Cycle' in row:
                legality_object['affects_full_cycle'] = row['Affects Full Cycle'] == "Yes"

            legality_object['date_announced'] = row['Date Announced']

            legality_object['date_in_effect'] = row['Date In Effect']

            if 'Planned End' in row:
                legality_object['planned_end'] = row['Planned End']

            legality_object['legality_article'] = row['Legality Article']

            legality_array.append(legality_object)

    json_object = json.dumps(legality_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {filename}.json\n")