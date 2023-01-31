import csv
import json
import re
from pathlib import Path
from markdown_patch import unmark

import helper_functions

def generate_json_file():
    print("Filling out english card.json from card.csv...")

    card_array = []


    setJsonPath = Path(__file__).parent / "../../../json/english/set.json"

    csvPath = Path(__file__).parent / "../../../csvs/english/card.csv"
    jsonPath = Path(__file__).parent / "../../../json/english/card.json"

    with (
        csvPath.open(newline='') as csvfile,
        setJsonPath.open(newline='') as set_json_file,
    ):
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        set_array = json.load(set_json_file)
        set_edition_unique_id_cache = {}

        for row in reader:
            card_object = {}

            rowId = 0

            card_object['unique_id'] = row[rowId]
            rowId += 1

            ids = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            set_ids = helper_functions.convert_to_array(row[rowId])
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

            rarities = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            card_object['types'] = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            card_object['card_keywords'] = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            card_object['abilities_and_effects'] = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            card_object['ability_and_effect_keywords'] = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            card_object['granted_keywords'] = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            card_object['functional_text'] = row[rowId]
            rowId += 1

            card_object['functional_text_plain'] = unmark(card_object['functional_text'])

            card_object['flavor_text'] = row[rowId]
            rowId += 1

            card_object['flavor_text_plain'] = unmark(card_object['flavor_text'])

            card_object['type_text'] = row[rowId]
            rowId += 1

            artists = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            card_object['played_horizontally'] = helper_functions.treat_string_as_boolean(row[rowId], default_value=False)
            rowId += 1

            card_object['blitz_legal'] = helper_functions.treat_string_as_boolean(row[rowId])
            rowId += 1

            card_object['cc_legal'] = helper_functions.treat_string_as_boolean(row[rowId])
            rowId += 1

            card_object['commoner_legal'] = helper_functions.treat_string_as_boolean(row[rowId])
            rowId += 1

            blitz_living_legend_field = row[rowId]
            card_object['blitz_living_legend'] = helper_functions.treat_blank_string_as_none(blitz_living_legend_field) != None
            if card_object['blitz_living_legend']:
                card_object['blitz_living_legend_start'] = blitz_living_legend_field
            rowId += 1

            cc_living_legend_field = row[rowId]
            card_object['cc_living_legend'] = helper_functions.treat_blank_string_as_none(cc_living_legend_field) != None
            if card_object['cc_living_legend']:
                card_object['cc_living_legend_start'] = cc_living_legend_field
            rowId += 1

            blitz_banned_field = row[rowId]
            card_object['blitz_banned'] = helper_functions.treat_blank_string_as_none(blitz_banned_field) != None
            if card_object['blitz_banned']:
                card_object['blitz_banned_start'] = blitz_banned_field
            rowId += 1

            cc_banned_field = row[rowId]
            card_object['cc_banned'] = helper_functions.treat_blank_string_as_none(cc_banned_field) != None
            if card_object['cc_banned']:
                card_object['cc_banned_start'] = cc_banned_field
            rowId += 1

            commoner_banned_field = row[rowId]
            card_object['commoner_banned'] = helper_functions.treat_blank_string_as_none(commoner_banned_field) != None
            if card_object['commoner_banned']:
                card_object['commoner_banned_start'] = commoner_banned_field
            rowId += 1

            upf_banned_field = row[rowId]
            card_object['upf_banned'] = helper_functions.treat_blank_string_as_none(upf_banned_field) != None
            if card_object['upf_banned']:
                card_object['upf_banned_start'] = upf_banned_field
            rowId += 1

            blitz_suspended_start_field = row[rowId]
            card_object['blitz_suspended'] = helper_functions.treat_blank_string_as_none(blitz_suspended_start_field) != None
            if card_object['blitz_suspended']:
                card_object['blitz_suspended_start'] = blitz_suspended_start_field
            rowId += 1

            if card_object['blitz_suspended']:
                card_object['blitz_suspended_end'] = row[rowId]
            rowId += 1

            cc_suspended_start_field = row[rowId]
            card_object['cc_suspended'] = helper_functions.treat_blank_string_as_none(cc_suspended_start_field) != None
            if card_object['cc_suspended']:
                card_object['cc_suspended_start'] = cc_suspended_start_field
            rowId += 1

            if card_object['cc_suspended']:
                card_object['cc_suspended_end'] = row[rowId]
            rowId += 1

            commoner_suspended_start_field = row[rowId]
            card_object['commoner_suspended'] = helper_functions.treat_blank_string_as_none(commoner_suspended_start_field) != None
            if card_object['commoner_suspended']:
                card_object['commoner_suspended_start'] = commoner_suspended_start_field
            rowId += 1

            if card_object['commoner_suspended']:
                card_object['commoner_suspended_end'] = row[rowId]
            rowId += 1

            variations = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            variation_unique_ids = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            image_urls = helper_functions.convert_to_array(row[rowId])
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

            image_url_data = [helper_functions.convert_image_data(x) for x in image_urls]
            unique_id_data = [helper_functions.convert_variation_unique_id_data(x) for x in variation_unique_ids]

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
                card_variation['set_edition_unique_id'] = helper_functions.get_set_edition_unique_id(set_id, set_edition, "english", set_array, set_edition_unique_id_cache)
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