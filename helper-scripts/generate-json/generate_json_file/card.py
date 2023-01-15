import csv
import json
import re
from pathlib import Path
from markdown_patch import unmark

def convert_to_array(field):
    return [x for x in field.split(", ") if x.strip() != ""]

def convert_image_data(image_url):
    image_url_split = re.split("— | – | - ", image_url.strip())

    image_url_data = {}
    image_url_data['image_url'] = image_url_split[0]
    image_url_data['card_id'] = image_url_split[1]
    image_url_data['set_edition'] = image_url_split[2]
    image_url_data['alternate_art_type'] = None
    if len(image_url_split) >= 4:
        image_url_data['alternate_art_type'] = image_url_split[3]

    return image_url_data

# TODO: Clean up redundant function
def convert_variation_unique_id_data(variation_unique_id):
    variation_unique_id_split = re.split("— | – | - ", variation_unique_id.strip())

    variation_unique_id_data = {}
    variation_unique_id_data['unique_id'] = variation_unique_id_split[0]
    variation_unique_id_data['card_id'] = variation_unique_id_split[1]
    variation_unique_id_data['set_edition'] = variation_unique_id_split[2]
    variation_unique_id_data['alternate_art_type'] = None
    if len(variation_unique_id_split) >= 4:
        variation_unique_id_data['alternate_art_type'] = variation_unique_id_split[3]

    return variation_unique_id_data

def treat_string_as_boolean(field, default_value=True):
    return bool(treat_blank_string_as_boolean(field, default_value))

def treat_blank_string_as_boolean(field, default_value=True):
    if field.strip() == '':
        return default_value

    return field

def treat_blank_string_as_none(field):
    if field == '':
        return None

    return field

def generate_json_file():
    print("Filling out english card.json from card.csv...")

    card_array = []

    csvPath = Path(__file__).parent / "../../../csvs/english/card.csv"
    jsonPath = Path(__file__).parent / "../../../json/english/card.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            card_object = {}

            rowId = 0

            card_object['unique_id'] = row[rowId]
            rowId += 1

            ids = convert_to_array(row[rowId])
            rowId += 1

            set_ids = convert_to_array(row[rowId])
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

            rarities = convert_to_array(row[rowId])
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

            card_object['functional_text_plain'] = unmark(card_object['functional_text'])

            card_object['flavor_text'] = row[rowId]
            rowId += 1

            card_object['flavor_text_plain'] = unmark(card_object['flavor_text'])

            card_object['type_text'] = row[rowId]
            rowId += 1

            artists = convert_to_array(row[rowId])
            rowId += 1

            card_object['played_horizontally'] = treat_string_as_boolean(row[rowId], default_value=False)
            rowId += 1

            card_object['blitz_legal'] = treat_string_as_boolean(row[rowId])
            rowId += 1

            card_object['cc_legal'] = treat_string_as_boolean(row[rowId])
            rowId += 1

            card_object['commoner_legal'] = treat_string_as_boolean(row[rowId])
            rowId += 1

            blitz_living_legend_field = row[rowId]
            card_object['blitz_living_legend'] = treat_blank_string_as_none(blitz_living_legend_field) != None
            if card_object['blitz_living_legend']:
                card_object['blitz_living_legend_start'] = blitz_living_legend_field
            rowId += 1

            cc_living_legend_field = row[rowId]
            card_object['cc_living_legend'] = treat_blank_string_as_none(cc_living_legend_field) != None
            if card_object['cc_living_legend']:
                card_object['cc_living_legend_start'] = cc_living_legend_field
            rowId += 1

            blitz_banned_field = row[rowId]
            card_object['blitz_banned'] = treat_blank_string_as_none(blitz_banned_field) != None
            if card_object['blitz_banned']:
                card_object['blitz_banned_start'] = blitz_banned_field
            rowId += 1

            cc_banned_field = row[rowId]
            card_object['cc_banned'] = treat_blank_string_as_none(cc_banned_field) != None
            if card_object['cc_banned']:
                card_object['cc_banned_start'] = cc_banned_field
            rowId += 1

            commoner_banned_field = row[rowId]
            card_object['commoner_banned'] = treat_blank_string_as_none(commoner_banned_field) != None
            if card_object['commoner_banned']:
                card_object['commoner_banned_start'] = commoner_banned_field
            rowId += 1

            upf_banned_field = row[rowId]
            card_object['upf_banned'] = treat_blank_string_as_none(upf_banned_field) != None
            if card_object['upf_banned']:
                card_object['upf_banned_start'] = upf_banned_field
            rowId += 1

            blitz_suspended_start_field = row[rowId]
            card_object['blitz_suspended'] = treat_blank_string_as_none(blitz_suspended_start_field) != None
            if card_object['blitz_suspended']:
                card_object['blitz_suspended_start'] = blitz_suspended_start_field
            rowId += 1

            if card_object['blitz_suspended']:
                card_object['blitz_suspended_end'] = row[rowId]
            rowId += 1

            cc_suspended_start_field = row[rowId]
            card_object['cc_suspended'] = treat_blank_string_as_none(cc_suspended_start_field) != None
            if card_object['cc_suspended']:
                card_object['cc_suspended_start'] = cc_suspended_start_field
            rowId += 1

            if card_object['cc_suspended']:
                card_object['cc_suspended_end'] = row[rowId]
            rowId += 1

            commoner_suspended_start_field = row[rowId]
            card_object['commoner_suspended'] = treat_blank_string_as_none(commoner_suspended_start_field) != None
            if card_object['commoner_suspended']:
                card_object['commoner_suspended_start'] = commoner_suspended_start_field
            rowId += 1

            if card_object['commoner_suspended']:
                card_object['commoner_suspended_end'] = row[rowId]
            rowId += 1

            variations = convert_to_array(row[rowId])
            rowId += 1

            variation_unique_ids = convert_to_array(row[rowId])
            rowId += 1

            image_urls = convert_to_array(row[rowId])
            rowId += 1

            # Clean up fields

            if card_object['played_horizontally'] == '':
                card_object['played_horizontally'] = False
            if card_object['blitz_legal'] == '':
                card_object['blitz_legal'] = True
            if card_object['cc_legal'] == '':
                card_object['cc_legal'] = True
            if card_object['commoner_legal'] == '':
                card_object['commoner_legal'] = True

            card_object['functional_text'] = card_object['functional_text'].replace("'", "''")
            card_object['functional_text_plain'] = card_object['functional_text_plain'].replace("'", "''")
            card_object['flavor_text'] = card_object['flavor_text'].replace("'", "''")
            card_object['flavor_text_plain'] = card_object['flavor_text_plain'].replace("'", "''")


            # Card Printings

            card_printing_array = []

            has_different_artists = len(artists) > 1
            artists_switched_mid_print = len([x for x in artists if " — " in x or " – " in x or " - " in x]) > 0
            rarities_switched_mid_print = len([x for x in rarities if " — " in x or " – " in x or " - " in x]) > 0

            image_url_data = [convert_image_data(x) for x in image_urls]
            unique_id_data = [convert_variation_unique_id_data(x) for x in variation_unique_ids]

            for variation_index, variation in enumerate(variations):
                card_variation = {}

                variation_split = re.split("— | – | - ", variation.strip())

                foilings = variation_split[0].strip().split(' ')
                card_id_from_variation = variation_split[1]
                set_edition = variation_split[2]
                alternative_art_type = None
                if len(variation_split) >= 4:
                    alternative_art_type = variation_split[3]

                cardIdIndex = ids.index(card_id_from_variation)

                set_id = set_ids[cardIdIndex]

                if has_different_artists:
                    if artists_switched_mid_print:
                        artist = artists[variation_index]

                        if len([x for x in artists if " — " in x or " – " in x or " - " in x]) > 0:
                            artist = re.split("— | – | - ", artist)[0]
                    else:
                        artist = artists[cardIdIndex]
                else:
                    artist = artists[0]

                if rarities_switched_mid_print:
                    rarity = rarities[variation_index]

                    if len([x for x in rarities if " — " in x or " – " in x or " - " in x]) > 0:
                            rarity = re.split("— | – | - ", rarity)[0]
                else:
                    rarity = rarities[0]

                valid_image_urls = [data for data in image_url_data if data['card_id'] == card_id_from_variation and data['set_edition'] == set_edition and data['alternate_art_type'] == alternative_art_type]
                image_url = valid_image_urls[0]['image_url'] if len(valid_image_urls) > 0 else None

                valid_unique_ids = [data for data in unique_id_data if data['card_id'] == card_id_from_variation and data['set_edition'] == set_edition and data['alternate_art_type'] == alternative_art_type]
                unique_id = valid_unique_ids[0]['unique_id'] if len(valid_unique_ids) > 0 else None

                card_variation['unique_id'] = unique_id
                card_variation['id'] = card_id_from_variation
                card_variation['set_id'] = set_id
                card_variation['edition'] = set_edition
                card_variation['foilings'] = foilings
                card_variation['rarity'] = rarity
                card_variation['artist'] = artist
                card_variation['art_variation'] = alternative_art_type
                card_variation['image_url'] = image_url

                card_printing_array.append(card_variation)

            card_object['printings'] = card_printing_array

            card_array.append(card_object)

    json_object = json.dumps(card_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print("Successfully generated english card.csv\n")