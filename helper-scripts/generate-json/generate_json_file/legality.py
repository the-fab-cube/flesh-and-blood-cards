import csv
import json
from pathlib import Path

def generate_json_file(filename):
    print(f"Generating {filename}.json from {filename}.csv...")

    legality_array = []

    csvPath = Path(__file__).parent / f"../../../csvs/english/{filename}.csv"
    jsonPath = Path(__file__).parent / f"../../../json/english/{filename}.json"

    suspended = "suspended" in filename

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            legality_object = {}

            rowId = 0

            legality_object['unique_id'] = row[rowId]
            rowId += 1

            legality_object['card_unique_id'] = row[rowId]
            rowId += 1
            rowId += 1
            rowId += 1

            status_active = True if row[rowId] == "Yes" else False if row[rowId] == "No" else None
            legality_object['status_active'] = status_active
            rowId += 1

            legality_object['date_announced'] = row[rowId]
            rowId += 1

            legality_object['date_in_effect'] = row[rowId]
            rowId += 1

            if suspended:
                legality_object['planned_end'] = row[rowId]
                rowId += 1

            legality_object['legality_article'] = row[rowId]
            rowId += 1

            legality_array.append(legality_object)

    json_object = json.dumps(legality_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {filename}.json\n")