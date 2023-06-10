import csv
import json
from markdown_patch import unmark

import helper_functions

def convert_printings_to_dict(card_printing_csv_path, card_face_association_json_path=None):
    # index is the card unique id
    card_printing_dict = {}

    with (
        card_printing_csv_path.open(newline='') as csvfile,
    ):
        reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')

        card_face_association_array = []

        if card_face_association_json_path is not None:
            with card_face_association_json_path.open(newline='') as card_face_association_json_file:
                card_face_association_array = json.load(card_face_association_json_file)

        for row in reader:
            card_variation = {}
            double_sided_card_info = []

            printing_unique_id = row['Unique ID']
            card_unique_id = row['Card Unique ID']

            for x in [x for x in card_face_association_array if x['front_unique_id'] == printing_unique_id]:
                double_sided_card_info.append(
                    {
                        'other_face_unique_id': x['back_unique_id'],
                        'is_front': True,
                        'is_DFC': x['is_DFC']
                    }
                )

            for x in [x for x in card_face_association_array if x['back_unique_id'] == printing_unique_id]:
                double_sided_card_info.append(
                    {
                        'other_face_unique_id': x['back_unique_id'],
                        'is_front': False,
                        'is_DFC': x['is_DFC']
                    }
                )

            card_variation['unique_id'] = printing_unique_id
            card_variation['set_edition_unique_id'] = row['Set Edition Unique ID']
            card_variation['id'] = row['Card ID']
            card_variation['set_id'] = row['Set ID']
            card_variation['edition'] = row['Edition']
            card_variation['foiling'] = row['Foiling']
            card_variation['rarity'] = row['Rarity']
            card_variation['artist'] = row['Artist']
            card_variation['art_variation'] = helper_functions.treat_blank_string_as_none(row['Art Variation'])
            card_variation['flavor_text'] = row['Flavor Text']
            card_variation['flavor_text_plain'] = unmark(card_variation['flavor_text'])
            card_variation['image_url'] = row['Image URL']
            if len(double_sided_card_info) > 0:
                card_variation['double_sided_card_info'] = double_sided_card_info

            if card_unique_id not in card_printing_dict:
                card_printing_dict[card_unique_id] = []

            card_printing_dict[card_unique_id].append(card_variation)

    return card_printing_dict