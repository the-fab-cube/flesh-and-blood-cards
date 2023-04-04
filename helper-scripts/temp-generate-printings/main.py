import csv
import json
from os.path import exists
from pathlib import Path
import re

import helper_functions

def create_csv_from_card_csv(language):
    print(f"Generating {language} card-printing.csv from {language} card.csv...")

    set_json_path = Path(__file__).parent / "../../json/english/set.json"

    # Compile list of unique printings from the card.csv
    card_printings = list()

    path = Path(__file__).parent / f"../../csvs/{language}/card.csv"
    with (path.open(newline='') as csvfile, set_json_path.open(newline='') as set_json_file):
        reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')

        set_array = json.load(set_json_file)
        set_edition_unique_id_cache = {}

        for row in reader:
            card_unique_id = row['Unique ID']
            name = row['Name']
            pitch = row['Pitch']
            flavor_text = row['Flavor Text']
            ids = helper_functions.convert_to_array(row['Identifiers'])
            set_ids = helper_functions.convert_to_array(row['Set Identifiers'])
            rarities = helper_functions.convert_to_array(row['Rarity'])
            artists = helper_functions.convert_to_array(row['Artists'])
            variations = helper_functions.convert_to_array(row['Variations'])
            variation_unique_ids = helper_functions.convert_to_array(row['Variation Unique IDs'])
            image_urls = helper_functions.convert_to_array(row['Image URLs'])

            # Card Printings

            has_different_artists = len(artists) > 1
            artists_switched_mid_print = len([x for x in artists if " — " in x or " – " in x or " - " in x]) > 0
            rarities_switched_mid_print = len([x for x in rarities if " — " in x or " – " in x or " - " in x]) > 0

            image_url_data = [helper_functions.convert_image_data(x) for x in image_urls]
            unique_id_data = [helper_functions.convert_variation_unique_id_data(x) for x in variation_unique_ids]

            for variation_index, variation in enumerate(variations):
                card_variation = {}

                card_variation['Card Unique ID'] = card_unique_id
                card_variation['Card Name'] = name
                card_variation['Card Pitch'] = pitch
                card_variation['Flavor Text'] = flavor_text

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

                card_variation['Unique ID'] = unique_id
                card_variation['Card Unique ID'] = card_unique_id
                card_variation['Card ID'] = card_id_from_variation
                card_variation['Set Unique ID'] = helper_functions.get_set_edition_unique_id(set_id, set_edition, "english", set_array, set_edition_unique_id_cache)
                card_variation['Set ID'] = set_id
                card_variation['Edition'] = set_edition
                card_variation['Rarity'] = rarity
                card_variation['Artist'] = artist
                card_variation['Art Variation'] = alternative_art_type
                card_variation['Image URL'] = image_url

                for index, foiling in enumerate(foilings):
                    printing_to_add = card_variation.copy()
                    printing_to_add['Foiling'] = foiling

                    if index != 0:
                        printing_to_add['Unique ID'] = None

                    card_printings.append(printing_to_add)

    # Output the sorted list of unique artists as a CSV
    path = Path(__file__).parent / f"../../csvs/{language}/card-printing.csv"
    with path.open('w', newline='') as csvout:
        fieldnames = [
            'Unique ID',
            'Card Unique ID',
            'Card Name',
            'Card Pitch',
            'Card ID',
            'Set Unique ID',
            'Set ID',
            'Edition',
            'Rarity',
            'Foiling',
            'Art Variation',
            'Artist',
            'Flavor Text',
            'Image URL',
        ]
        writer = csv.DictWriter(csvout, delimiter="\t", lineterminator="\n", fieldnames=fieldnames)

        # Add title row
        writer.writeheader()

        for card_printing in sorted(card_printings, key=lambda item: item['Set ID']):
            writer.writerow(card_printing)

    print(f"Successfully generated {language} card-printing.csv")



create_csv_from_card_csv("english")
# create_csv_from_card_csv("french")
# create_csv_from_card_csv("german")
# create_csv_from_card_csv("italian")
# create_csv_from_card_csv("spanish")
