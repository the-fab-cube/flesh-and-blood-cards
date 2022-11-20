import csv
import json
from pathlib import Path

def convert_to_null(field):
    if field.strip().lower() == "null":
        return None
    else:
        return field

def convert_to_array(field):
    return [convert_to_null(x) for x in field.split(", ") if x.strip() != ""]

def generate_json_file():
    print("Generating set.json from set.csv...")

    set_array = []

    csvPath = Path(__file__).parent / "../../csvs/set.csv"
    jsonPath = Path(__file__).parent / "../../json/set.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            set_object = {}

            set_object['id'] = row[0]
            set_object['name'] = row[1]
            editions = convert_to_array(row[2])
            initial_release_dates = convert_to_array(row[3]) # row[3].lower().replace("null", "infinity") # Uses infinity instead of null because some parsers break parsing timestamp arrays with null
            out_of_print_dates = convert_to_array(row[4]) # row[4].lower().replace("null", "infinity") # Uses infinity instead of null because some parsers break parsing timestamp arrays with null

            set_object['start_card_id'] = row[5]
            set_object['end_card_id'] = row[6]

            product_pages = convert_to_array(row[7])
            collectors_center = convert_to_array(row[8])
            card_galleries = convert_to_array(row[9])

            editions_array = []

            for index, edition in enumerate(editions):
                edition_object = {}

                edition_object['edition'] = edition
                edition_object['initial_release_date'] = initial_release_dates[index]
                edition_object['out_of_print_date'] = out_of_print_dates[index]
                edition_object['product_page'] = product_pages[index]
                edition_object['collectors_center'] = collectors_center[index]
                edition_object['card_gallery'] = card_galleries[index]

                editions_array.append(edition_object)

            set_object['editions'] = editions_array

            set_array.append(set_object)

    json_object = json.dumps(set_array, indent=4)

    with jsonPath.open('w', newline='\n') as outfile:
        outfile.write(json_object)

    print("Successfully generated set.json\n")