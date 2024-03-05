import csv
import json
from pathlib import Path
from markdown_patch import unmark

import convert_card_printings_to_dict
import helper_functions

def generate_json_file():
    print("Filling out english card.json from card.csv...")

    card_array = []

    card_json_path = Path(__file__).parent / "../../../json/english/card.json"
    card_face_association_json_path = Path(__file__).parent / "../../../json/english/card-face-association.json"
    card_reference_json_path = Path(__file__).parent / "../../../json/english/card-reference.json"
    banned_blitz_json_path = Path(__file__).parent / "../../../json/english/banned-blitz.json"
    banned_cc_json_path = Path(__file__).parent / "../../../json/english/banned-cc.json"
    banned_commoner_json_path = Path(__file__).parent / "../../../json/english/banned-commoner.json"
    banned_upf_json_path = Path(__file__).parent / "../../../json/english/banned-upf.json"
    living_legend_blitz_json_path = Path(__file__).parent / "../../../json/english/living-legend-blitz.json"
    living_legend_cc_json_path = Path(__file__).parent / "../../../json/english/living-legend-cc.json"
    suspended_blitz_json_path = Path(__file__).parent / "../../../json/english/suspended-blitz.json"
    suspended_cc_json_path = Path(__file__).parent / "../../../json/english/suspended-cc.json"
    suspended_commoner_json_path = Path(__file__).parent / "../../../json/english/suspended-commoner.json"
    ll_restricted_json_path = Path(__file__).parent / "../../../json/english/restricted-ll.json"

    card_csv_path = Path(__file__).parent / "../../../csvs/english/card.csv"
    card_printing_csv_path = Path(__file__).parent / "../../../csvs/english/card-printing.csv"

    card_printing_dict = convert_card_printings_to_dict.convert_card_printings_to_dict("english", card_printing_csv_path, card_face_association_json_path)

    with (
        card_csv_path.open(newline='') as csvfile,
        card_reference_json_path.open(newline='') as card_reference_json_file,
        banned_blitz_json_path.open(newline='') as banned_blitz_json_file,
        banned_cc_json_path.open(newline='') as banned_cc_json_file,
        banned_commoner_json_path.open(newline='') as banned_commoner_json_file,
        banned_upf_json_path.open(newline='') as banned_upf_json_file,
        living_legend_blitz_json_path.open(newline='') as living_legend_blitz_json_file,
        living_legend_cc_json_path.open(newline='') as living_legend_cc_json_file,
        suspended_blitz_json_path.open(newline='') as suspended_blitz_json_file,
        suspended_cc_json_path.open(newline='') as suspended_cc_json_file,
        suspended_commoner_json_path.open(newline='') as suspended_commoner_json_file,
        ll_restricted_json_path.open(newline='') as ll_restricted_json_file,
    ):
        reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')

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
        ll_restricted_array = json.load(ll_restricted_json_file)

        for row in reader:
            card_object = {}

            card_unique_id = row['Unique ID']
            card_object['unique_id'] = card_unique_id

            card_object['name'] = row['Name']
            card_object['pitch'] = row['Pitch']
            card_object['cost'] = row['Cost']
            card_object['power'] = row['Power']
            card_object['defense'] = row['Defense']
            card_object['health'] = row['Health']
            card_object['intelligence'] = row['Intelligence']

            card_object['types'] = helper_functions.convert_to_array(row['Types'])
            card_object['card_keywords'] = helper_functions.convert_to_array(row['Card Keywords'])
            card_object['abilities_and_effects'] = helper_functions.convert_to_array(row['Abilities and Effects'])
            card_object['ability_and_effect_keywords'] = helper_functions.convert_to_array(row['Ability and Effect Keywords'])
            card_object['granted_keywords'] = helper_functions.convert_to_array(row['Granted Keywords'])
            card_object['removed_keywords'] = helper_functions.convert_to_array(row['Removed Keywords'])
            card_object['interacts_with_keywords'] = helper_functions.convert_to_array(row['Interacts with Keywords'])

            card_object['functional_text'] = row['Functional Text']
            card_object['functional_text_plain'] = unmark(card_object['functional_text'])

            card_object['type_text'] = row['Type Text']
            card_object['played_horizontally'] = helper_functions.treat_string_as_boolean(row['Card Played Horizontally'], default_value=False)
            card_object['blitz_legal'] = helper_functions.treat_string_as_boolean(row['Blitz Legal'])
            card_object['cc_legal'] = helper_functions.treat_string_as_boolean(row['CC Legal'])
            card_object['commoner_legal'] = helper_functions.treat_string_as_boolean(row['Commoner Legal'])

            living_legend_blitz_info_array = [x for x in living_legend_blitz_array if x['card_unique_id'] == card_unique_id]
            living_legend_blitz_info = living_legend_blitz_info_array[-1] if len(living_legend_blitz_info_array) > 0 else None
            card_object['blitz_living_legend'] = living_legend_blitz_info['status_active'] if living_legend_blitz_info != None else False
            if card_object['blitz_living_legend']:
                card_object['blitz_living_legend_start'] = living_legend_blitz_info['date_in_effect']

            living_legend_cc_info_array = [x for x in living_legend_cc_array if x['card_unique_id'] == card_unique_id]
            living_legend_cc_info = living_legend_cc_info_array[-1] if len(living_legend_cc_info_array) > 0 else None
            card_object['cc_living_legend'] = living_legend_cc_info['status_active'] if living_legend_cc_info != None else False
            if card_object['cc_living_legend']:
                card_object['cc_living_legend_start'] = living_legend_cc_info['date_in_effect']

            banned_blitz_info_array = [x for x in banned_blitz_array if x['card_unique_id'] == card_unique_id]
            banned_blitz_info = banned_blitz_info_array[-1] if len(banned_blitz_info_array) > 0 else None
            card_object['blitz_banned'] = banned_blitz_info['status_active'] if banned_blitz_info != None else False
            if card_object['blitz_banned']:
                card_object['blitz_banned_start'] = banned_blitz_info['date_in_effect']

            banned_cc_info_array = [x for x in banned_cc_array if x['card_unique_id'] == card_unique_id]
            banned_cc_info = banned_cc_info_array[-1] if len(banned_cc_info_array) > 0 else None
            card_object['cc_banned'] = banned_cc_info['status_active'] if banned_cc_info != None else False
            if card_object['cc_banned']:
                card_object['cc_banned_start'] = banned_cc_info['date_in_effect']

            banned_commoner_info_array = [x for x in banned_commoner_array if x['card_unique_id'] == card_unique_id]
            banned_commoner_info = banned_commoner_info_array[-1] if len(banned_commoner_info_array) > 0 else None
            card_object['commoner_banned'] = banned_commoner_info['status_active'] if banned_commoner_info != None else False
            if card_object['commoner_banned']:
                card_object['commoner_banned_start'] = banned_commoner_info['date_in_effect']

            banned_upf_info_array = [x for x in banned_upf_array if x['card_unique_id'] == card_unique_id]
            banned_upf_info = banned_upf_info_array[-1] if len(banned_upf_info_array) > 0 else None
            card_object['upf_banned'] = banned_upf_info['status_active'] if banned_upf_info != None else False
            if card_object['upf_banned']:
                card_object['upf_banned_start'] = banned_upf_info['date_in_effect']

            suspended_blitz_info_array = [x for x in suspended_blitz_array if x['card_unique_id'] == card_unique_id]
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

            suspended_cc_info_array = [x for x in suspended_cc_array if x['card_unique_id'] == card_unique_id]
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

            suspended_commoner_info_array = [x for x in suspended_commoner_array if x['card_unique_id'] == card_unique_id]
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
                
            ll_restricted_info_array = [x for x in ll_restricted_array if x['card_unique_id'] == card_unique_id]
            ll_restricted_info = ll_restricted_info_array[-1] if len(ll_restricted_info_array) > 0 else None
            card_object['ll_restricted'] = ll_restricted_info['status_active'] if ll_restricted_info != None else False
            if card_object['ll_restricted']:
                card_object['ll_restricted_start'] = ll_restricted_info['date_in_effect']

            # Clean up fields

            if card_object['played_horizontally'] == '':
                card_object['played_horizontally'] = False
            if card_object['blitz_legal'] == '':
                card_object['blitz_legal'] = True
            if card_object['cc_legal'] == '':
                card_object['cc_legal'] = True
            if card_object['commoner_legal'] == '':
                card_object['commoner_legal'] = True

            # card_object['functional_text'] = card_object['functional_text']
            # card_object['functional_text_plain'] = card_object['functional_text_plain']

            referenced_cards = []
            cards_referenced_by = []

            for x in [x for x in card_reference_array]:
                if x['card_unique_id'] == card_unique_id:
                    referenced_cards.append(x['referenced_card_unique_id'])

                if x['referenced_card_unique_id'] == card_unique_id:
                    cards_referenced_by.append(x['card_unique_id'])

            if len(referenced_cards) > 0:
                card_object['referenced_cards'] = referenced_cards

            if len(cards_referenced_by) > 0:
                card_object['cards_referenced_by'] = cards_referenced_by


            # Card Printings

            card_printing_array = card_printing_dict[card_unique_id]

            card_object['printings'] = card_printing_array

            card_array.append(card_object)

    json_object = json.dumps(card_array, indent=4, ensure_ascii=False)

    with card_json_path.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print("Successfully generated english card.csv\n")