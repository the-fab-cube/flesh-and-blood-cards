import csv
import json
import urllib.parse
from markdown_patch import unmark

import helper_functions

def convert_card_printings_to_dict(language, card_printing_csv_path, card_face_association_json_path=None):
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
            card_printing = {}
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

            tcgplayer_product_id = helper_functions.treat_blank_string_as_none(row['TCGPlayer ID'])
            edition = row['Edition']
            foiling = row['Foiling']

            card_printing['unique_id'] = printing_unique_id
            card_printing['set_printing_unique_id'] = row['Set Printing Unique ID']
            card_printing['id'] = row['Card ID']
            card_printing['set_id'] = row['Set ID']
            card_printing['edition'] = row['Edition']
            card_printing['foiling'] = row['Foiling']
            card_printing['rarity'] = row['Rarity']
            card_printing['artist'] = row['Artist']
            card_printing['art_variation'] = helper_functions.treat_blank_string_as_none(row['Art Variation'])
            card_printing['flavor_text'] = row['Flavor Text']
            card_printing['flavor_text_plain'] = unmark(card_printing['flavor_text'])
            card_printing['image_url'] = helper_functions.treat_blank_string_as_none(row['Image URL'])

            if tcgplayer_product_id is not None:
                card_printing['tcgplayer_product_id'] = tcgplayer_product_id
                card_printing['tcgplayer_url'] = create_tcgplayer_link(tcgplayer_product_id, language, edition, foiling)

            if len(double_sided_card_info) > 0:
                card_printing['double_sided_card_info'] = double_sided_card_info

            if card_unique_id not in card_printing_dict:
                card_printing_dict[card_unique_id] = []

            card_printing_dict[card_unique_id].append(card_printing)

    return card_printing_dict

def create_tcgplayer_link(product_id, language, edition, foiling):
    query = {}

    query['Language'] = language.capitalize()

    printing = create_tcgplayer_printing(edition, foiling)

    if printing is not None:
        query['Printing'] = printing

    return urllib.parse.urlunsplit(("https", "www.tcgplayer.com", f"/product/{product_id}", urllib.parse.urlencode(query), ""))

def create_tcgplayer_printing(edition, foiling):
    if edition is None and foiling is None:
        return None

    printing = ""
    edition_text = create_tcgplayer_edition_text(edition)
    foiling_text = create_tcgplayer_foiling_text(foiling)

    if edition_text is not None:
        printing += edition_text

    if foiling_text is not None:
        if printing != "":
            printing += " "
        printing += foiling_text

    return printing

def create_tcgplayer_edition_text(edition):
    match edition:
        case "A" | "F":
            return "1st Edition"
        case "U":
            return "Unlimited Edition"
        case _:
            return None

def create_tcgplayer_foiling_text(foiling):
    match foiling:
        case "S":
            return "Normal"
        case "R":
            return "Rainbow Foil"
        case "C":
            return "Cold Foil"
        case _:
            return None