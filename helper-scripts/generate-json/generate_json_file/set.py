import csv
import json
import re
from pathlib import Path

def convert_to_null(field):
    if field.strip().lower() == "null":
        return None
    else:
        return field

def convert_to_array(field):
    return [convert_to_null(x) for x in field.split(", ") if x.strip() != ""]

# TODO: Clean up redundant function
def convert_edition_unique_id_data(edition_unique_id):
    edition_unique_id_split = re.split("— | – | - ", edition_unique_id.strip())

    edition_unique_id_data = {}
    edition_unique_id_data['unique_id'] = edition_unique_id_split[0]
    edition_unique_id_data['edition'] = edition_unique_id_split[1]

    return edition_unique_id_data

def generate_json_file(language):
    print(f"Generating {language} set.json from set.csv...")

    set_array = []

    csvPath = Path(__file__).parent / f"../../../csvs/{language}/set.csv"
    jsonPath = Path(__file__).parent / f"../../../json/{language}/set.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            set_object = {}

            rowId = 0

            set_object['id'] = row[rowId]
            rowId += 1

            set_object['name'] = row[rowId]
            rowId += 1

            editions = convert_to_array(row[rowId])
            rowId += 1

            edition_unique_ids = convert_to_array(row[rowId])
            rowId += 1

            initial_release_dates = convert_to_array(row[rowId])
            rowId += 1

            out_of_print_dates = convert_to_array(row[rowId])
            rowId += 1

            set_object['start_card_id'] = row[rowId]
            rowId += 1

            set_object['end_card_id'] = row[rowId]
            rowId += 1

            product_pages = convert_to_array(row[rowId])
            rowId += 1

            collectors_center = convert_to_array(row[rowId])
            rowId += 1

            card_galleries = convert_to_array(row[rowId])
            rowId += 1

            editions_array = []

            unique_id_data = [convert_edition_unique_id_data(x) for x in edition_unique_ids]

            for index, edition in enumerate(editions):
                edition_object = {}

                valid_unique_ids = [data for data in unique_id_data if data['edition'] == edition]
                unique_id = valid_unique_ids[0]['unique_id'] if len(valid_unique_ids) > 0 else None

                edition_object['unique_id'] = unique_id
                edition_object['edition'] = edition
                edition_object['initial_release_date'] = initial_release_dates[index]
                edition_object['out_of_print_date'] = out_of_print_dates[index]
                edition_object['product_page'] = product_pages[index]
                edition_object['collectors_center'] = collectors_center[index]
                edition_object['card_gallery'] = card_galleries[index]

                editions_array.append(edition_object)

            set_object['editions'] = editions_array

            set_array.append(set_object)

    json_object = json.dumps(set_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {language} set.json\n")