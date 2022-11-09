import csv
import json
from pathlib import Path
from markdown_patch import unmark

def convert_to_array(field):
    return [x for x in field.split(", ") if x.strip() != ""]

def treat_string_as_boolean(field):
    return bool(treat_blank_string_as_boolean(field))

def treat_blank_string_as_boolean(field, value=True):
    if field == '':
        return value

    return field

def treat_blank_string_as_none(field):
    if field == '':
        return None

    return None

def generate_json_file():
    print("Filling out card.json from card.csv...\n")

    card_array = []

    csvPath = Path(__file__).parent / "../../csvs/card.csv"
    jsonPath = Path(__file__).parent / "../../json/card.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            card_object = {}

            rowId = 0

            card_object['ids'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['set_ids'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['name'] = row[rowId]
            rowId += 1

            card_object['pitch'] = row[rowId]
            rowId += 1

            card_object['cost'] = row[rowId]
            rowId += 1

            card_object['power'] = row[rowId]
            rowId += 1

            card_object['defense'] = row[rowId]
            rowId += 1

            card_object['health'] = row[rowId]
            rowId += 1

            card_object['intelligence'] = row[rowId]
            rowId += 1

            card_object['rarities'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['types'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['card_keywords'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['abilities_and_effects'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['ability_and_effect_keywords'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['granted_keywords'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['functional_text'] = row[rowId]
            rowId += 1

            card_object['flavor_text'] = row[rowId]
            rowId += 1

            card_object['type_text'] = row[rowId]
            rowId += 1

            card_object['artists'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['played_horizontally'] = row[rowId]
            rowId += 1

            card_object['blitz_legal'] = treat_string_as_boolean(row[rowId])
            rowId += 1

            card_object['cc_legal'] = treat_string_as_boolean(row[rowId])
            rowId += 1

            card_object['commoner_legal'] = treat_string_as_boolean(row[rowId])
            rowId += 1

            card_object['blitz_living_legend'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['cc_living_legend'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['blitz_banned'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['cc_banned'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['commoner_banned'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['upf_banned'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['blitz_suspended_start'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['blitz_suspended_end'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['cc_suspended_start'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['cc_suspended_end'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['commoner_suspended_start'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['commoner_suspended_end'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['variations'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['image_urls'] = convert_to_array(row[rowId])
            rowId += 1

            if card_object['played_horizontally'] == '':
                card_object['played_horizontally'] = False
            if card_object['blitz_legal'] == '':
                card_object['blitz_legal'] = True
            if card_object['cc_legal'] == '':
                card_object['cc_legal'] = True
            if card_object['commoner_legal'] == '':
                card_object['commoner_legal'] = True

            # functional_text_plain = unmark(functional_text)
            # flavor_text_plain = unmark(flavor_text)

            card_object['functional_text'] = card_object['functional_text'].replace("'", "''")
            # functional_text_plain = functional_text_plain.replace("'", "''")
            card_object['flavor_text'] = card_object['flavor_text'].replace("'", "''")
            # flavor_text_plain = flavor_text_plain.replace("'", "''")

            card_array.append(card_object)

    json_object = json.dumps(card_array, indent=4)

    with jsonPath.open('w', newline='\n') as outfile:
        outfile.write(json_object)

    print("\nSuccessfully generated card.csv\n")