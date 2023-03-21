import csv
import json
import re
from pathlib import Path
from markdown_patch import unmark

import helper_functions

def generate_json_file():
    print("Filling out english card.json from card.csv...")

    card_array = []

    set_json_path = Path(__file__).parent / "../../../json/english/set.json"
    card_face_association_json_path = Path(__file__).parent / "../../../json/english/card-face-association.json"
    card_refrence_json_path = Path(__file__).parent / "../../../json/english/card-reference.json"
    banned_blitz_json_path = Path(__file__).parent / "../../../json/english/banned-blitz.json"
    banned_cc_json_path = Path(__file__).parent / "../../../json/english/banned-cc.json"
    banned_commoner_json_path = Path(__file__).parent / "../../../json/english/banned-commoner.json"
    banned_upf_json_path = Path(__file__).parent / "../../../json/english/banned-upf.json"
    living_legend_blitz_json_path = Path(__file__).parent / "../../../json/english/living-legend-blitz.json"
    living_legend_cc_json_path = Path(__file__).parent / "../../../json/english/living-legend-cc.json"
    suspended_blitz_json_path = Path(__file__).parent / "../../../json/english/suspended-blitz.json"
    suspended_cc_json_path = Path(__file__).parent / "../../../json/english/suspended-cc.json"
    suspended_commoner_json_path = Path(__file__).parent / "../../../json/english/suspended-commoner.json"

    csvPath = Path(__file__).parent / "../../../csvs/english/card.csv"
    jsonPath = Path(__file__).parent / "../../../json/english/card.json"

    with (
        csvPath.open(newline='') as csvfile,
        set_json_path.open(newline='') as set_json_file,
        card_face_association_json_path.open(newline='') as card_face_association_json_file,
        card_refrence_json_path.open(newline='') as card_reference_json_file,
        banned_blitz_json_path.open(newline='') as banned_blitz_json_file,
        banned_cc_json_path.open(newline='') as banned_cc_json_file,
        banned_commoner_json_path.open(newline='') as banned_commoner_json_file,
        banned_upf_json_path.open(newline='') as banned_upf_json_file,
        living_legend_blitz_json_path.open(newline='') as living_legend_blitz_json_file,
        living_legend_cc_json_path.open(newline='') as living_legend_cc_json_file,
        suspended_blitz_json_path.open(newline='') as suspended_blitz_json_file,
        suspended_cc_json_path.open(newline='') as suspended_cc_json_file,
        suspended_commoner_json_path.open(newline='') as suspended_commoner_json_file,
    ):
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        set_array = json.load(set_json_file)
        card_face_association_array = json.load(card_face_association_json_file)
        card_reference_array = json.load(card_reference_json_file)
        banned_blitz_array = json.load(banned_blitz_json_file)
        banned_cc_array = json.load(banned_cc_json_file)
        banned_commoner_array = json.load(banned_commoner_json_file)
        banned_upf_array = json.load(banned_upf_json_file)
        living_legend_blitz_array = json.load(living_legend_blitz_json_file)
        living_legend_cc_array = json.load(living_legend_cc_json_file)
        suspended_blitz_array = json.load(suspended_blitz_json_file)
        suspended_cc_array = json.load(suspended_cc_json_file)
        suspended_commoner_array = json.load(suspended_commoner_json_file)
        set_edition_unique_id_cache = {}

        for row in reader:
            card_object = {}

            rowId = 0

            unique_id = row[rowId]
            card_object['unique_id'] = unique_id
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

            living_legend_blitz_info_array = [x for x in living_legend_blitz_array if x['card_unique_id'] == unique_id]
            living_legend_blitz_info = living_legend_blitz_info_array[-1] if len(living_legend_blitz_info_array) > 0 else None
            card_object['blitz_living_legend'] = living_legend_blitz_info['status_active'] if living_legend_blitz_info != None else False
            if card_object['blitz_living_legend']:
                card_object['blitz_living_legend_start'] = living_legend_blitz_info['date_in_effect']

            living_legend_cc_info_array = [x for x in living_legend_cc_array if x['card_unique_id'] == unique_id]
            living_legend_cc_info = living_legend_cc_info_array[-1] if len(living_legend_cc_info_array) > 0 else None
            card_object['cc_living_legend'] = living_legend_cc_info['status_active'] if living_legend_cc_info != None else False
            if card_object['cc_living_legend']:
                card_object['cc_living_legend_start'] = living_legend_cc_info['date_in_effect']

            banned_blitz_info_array = [x for x in banned_blitz_array if x['card_unique_id'] == unique_id]
            banned_blitz_info = banned_blitz_info_array[-1] if len(banned_blitz_info_array) > 0 else None
            card_object['blitz_banned'] = banned_blitz_info['status_active'] if banned_blitz_info != None else False
            if card_object['blitz_banned']:
                card_object['blitz_banned_start'] = banned_blitz_info['date_in_effect']

            banned_cc_info_array = [x for x in banned_cc_array if x['card_unique_id'] == unique_id]
            banned_cc_info = banned_cc_info_array[-1] if len(banned_cc_info_array) > 0 else None
            card_object['cc_banned'] = banned_cc_info['status_active'] if banned_cc_info != None else False
            if card_object['cc_banned']:
                card_object['cc_banned_start'] = banned_cc_info['date_in_effect']

            banned_commoner_info_array = [x for x in banned_commoner_array if x['card_unique_id'] == unique_id]
            banned_commoner_info = banned_commoner_info_array[-1] if len(banned_commoner_info_array) > 0 else None
            card_object['commoner_banned'] = banned_commoner_info['status_active'] if banned_commoner_info != None else False
            if card_object['commoner_banned']:
                card_object['commoner_banned_start'] = banned_commoner_info['date_in_effect']

            banned_upf_info_array = [x for x in banned_upf_array if x['card_unique_id'] == unique_id]
            banned_upf_info = banned_upf_info_array[-1] if len(banned_upf_info_array) > 0 else None
            card_object['upf_banned'] = banned_upf_info['status_active'] if banned_upf_info != None else False
            if card_object['upf_banned']:
                card_object['upf_banned_start'] = banned_upf_info['date_in_effect']

            suspended_blitz_info_array = [x for x in suspended_blitz_array if x['card_unique_id'] == unique_id]
            suspended_blitz_info = suspended_blitz_info_array[-1] if len(suspended_blitz_info_array) > 0 else None
            card_object['blitz_suspended'] = suspended_blitz_info['status_active'] if suspended_blitz_info != None else False
            if card_object['blitz_suspended']:
                start_info = suspended_blitz_info

                # Loop backwards through the info array and find when the card originally was suspended this time
                for info in suspended_blitz_info_array[::-1]:
                    if not info['status_active']:
                        break

                    start_info = info

                card_object['blitz_suspended_start'] = start_info['date_in_effect']
                card_object['blitz_suspended_end'] = suspended_blitz_info['planned_end']

            suspended_cc_info_array = [x for x in suspended_cc_array if x['card_unique_id'] == unique_id]
            suspended_cc_info = suspended_cc_info_array[-1] if len(suspended_cc_info_array) > 0 else None
            card_object['cc_suspended'] = suspended_cc_info['status_active'] if suspended_cc_info != None else False
            if card_object['cc_suspended']:
                start_info = suspended_cc_info

                # Loop backwards through the info array and find when the card originally was suspended this time
                for info in suspended_cc_info_array[::-1]:
                    if not info['status_active']:
                        break

                    start_info = info

                card_object['cc_suspended_start'] = start_info['date_in_effect']
                card_object['cc_suspended_end'] = suspended_cc_info['planned_end']

            suspended_commoner_info_array = [x for x in suspended_commoner_array if x['card_unique_id'] == unique_id]
            suspended_commoner_info = suspended_commoner_info_array[-1] if len(suspended_commoner_info_array) > 0 else None
            card_object['commoner_suspended'] = suspended_commoner_info['status_active'] if suspended_commoner_info != None else False
            if card_object['commoner_suspended']:
                start_info = suspended_commoner_info

                # Loop backwards through the info array and find when the card originally was suspended this time
                for info in suspended_commoner_info_array[::-1]:
                    if not info['status_active']:
                        break

                    start_info = info

                card_object['commoner_suspended_start'] = start_info['date_in_effect']
                card_object['commoner_suspended_end'] = suspended_commoner_info['planned_end']

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

            card_object['functional_text'] = card_object['functional_text']
            card_object['functional_text_plain'] = card_object['functional_text_plain']
            card_object['flavor_text'] = card_object['flavor_text']
            card_object['flavor_text_plain'] = card_object['flavor_text_plain']

            referenced_cards = []
            cards_referenced_by = []

            for x in [x for x in card_reference_array]:
                if x['card_unique_id'] == unique_id:
                    referenced_cards.append(x['referenced_card_unique_id'])

                if x['referenced_card_unique_id'] == unique_id:
                    cards_referenced_by.append(x['card_unique_id'])

            if len(referenced_cards) > 0:
                card_object['referenced_cards'] = referenced_cards

            if len(cards_referenced_by) > 0:
                card_object['cards_referenced_by'] = cards_referenced_by


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
                    rarity = rarities[cardIdIndex]

                valid_image_urls = [data for data in image_url_data if data['card_id'] == card_id_from_variation and data['set_edition'] == set_edition and data['alternate_art_type'] == alternative_art_type]
                image_url = valid_image_urls[0]['image_url'] if len(valid_image_urls) > 0 else None

                valid_unique_ids = [data for data in unique_id_data if data['card_id'] == card_id_from_variation and data['set_edition'] == set_edition and data['alternate_art_type'] == alternative_art_type]
                unique_id = valid_unique_ids[0]['unique_id'] if len(valid_unique_ids) > 0 else None

                double_sided_card_info = []

                for x in [x for x in card_face_association_array if x['front_unique_id'] == unique_id]:
                    double_sided_card_info.append(
                        {
                            'other_face_unique_id': x['back_unique_id'],
                            'is_front': True,
                            'is_DFC': x['is_DFC']
                        }
                    )

                for x in [x for x in card_face_association_array if x['back_unique_id'] == unique_id]:
                    double_sided_card_info.append(
                        {
                            'other_face_unique_id': x['back_unique_id'],
                            'is_front': False,
                            'is_DFC': x['is_DFC']
                        }
                    )

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
                if len(double_sided_card_info) > 0:
                    card_variation['double_sided_card_info'] = double_sided_card_info

                card_printing_array.append(card_variation)

            card_object['printings'] = card_printing_array

            card_array.append(card_object)

    json_object = json.dumps(card_array, indent=4, ensure_ascii=False)

    with jsonPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print("Successfully generated english card.csv\n")