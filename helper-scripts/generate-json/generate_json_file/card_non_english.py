import csv
import json
import re
from pathlib import Path
from markdown_patch import unmark

import helper_functions
import convert_english_abilities_to_language
import convert_english_keywords_to_language
import convert_english_types_to_language

def generate_json_file(language):
    print(f"Filling out {language} card.json from card.csv...")

    card_array = []

    english_json_path = Path(__file__).parent / "../../../json/english/card.json"
    english_ability_json_path = Path(__file__).parent / f"../../../json/english/ability.json"
    english_keyword_json_path = Path(__file__).parent / f"../../../json/english/keyword.json"
    english_type_json_path = Path(__file__).parent / f"../../../json/english/type.json"

    language_csv_path = Path(__file__).parent / f"../../../csvs/{language}/card.csv"
    language_card_json_path = Path(__file__).parent / f"../../../json/{language}/card.json"
    language_ability_json_path = Path(__file__).parent / f"../../../json/{language}/ability.json"
    language_keyword_json_path = Path(__file__).parent / f"../../../json/{language}/keyword.json"
    language_set_json_path = Path(__file__).parent / f"../../../json/{language}/set.json"
    language_type_json_path = Path(__file__).parent / f"../../../json/{language}/type.json"

    with (
        language_csv_path.open(newline='') as csv_file,
        english_json_path.open(newline='') as english_card_json_file,
        english_ability_json_path.open(newline='') as english_ability_json_file,
        english_keyword_json_path.open(newline='') as english_keyword_json_file,
        english_type_json_path.open(newline='') as english_type_json_file,
        language_ability_json_path.open(newline='') as language_ability_json_file,
        language_keyword_json_path.open(newline='') as language_keyword_json_file,
        language_set_json_path.open(newline='') as language_set_json_file,
        language_type_json_path.open(newline='') as language_type_json_file
    ):
        english_card_array = json.load(english_card_json_file)
        english_ability_array = json.load(english_ability_json_file)
        english_keyword_array = json.load(english_keyword_json_file)
        english_type_array = json.load(english_type_json_file)
        language_ability_array = json.load(language_ability_json_file)
        language_keyword_array = json.load(language_keyword_json_file)
        language_set_array = json.load(language_set_json_file)
        language_type_array = json.load(language_type_json_file)

        set_unique_id_cache = {}

        reader = csv.reader(csv_file, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            card_object = {}

            rowId = 0

            unique_id = row[rowId]

            card_object['unique_id'] = unique_id
            # assumes there is an english card - script will throw an exception otherwise
            english_card = [x for x in english_card_array if x['unique_id'] == unique_id][0]
            rowId += 1

            ids = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            set_ids = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            card_object['name'] = row[rowId]
            rowId += 1

            card_object['pitch'] = english_card['pitch']
            card_object['cost'] = english_card['cost']
            card_object['power'] = english_card['power']
            card_object['defense'] = english_card['defense']
            card_object['health'] = english_card['health']
            card_object['intelligence'] = english_card['intelligence']

            rarities = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            english_card_types = english_card['types']
            card_object['types'] = convert_english_types_to_language.convert_english_types_to_language(language, english_card_types, english_type_array, language_type_array)

            english_card_keywords = english_card['card_keywords']
            card_object['card_keywords'] = convert_english_keywords_to_language.convert_english_keywords_to_language(language, english_card_keywords, english_keyword_array, language_keyword_array)

            english_card_abilities = english_card['abilities_and_effects']
            card_object['abilities_and_effects'] = convert_english_abilities_to_language.convert_english_abilities_to_language(language, english_card_abilities, english_ability_array, language_ability_array)

            english_card_ability_and_effect_keywords = english_card['ability_and_effect_keywords']
            card_object['ability_and_effect_keywords'] = convert_english_keywords_to_language.convert_english_keywords_to_language(language, english_card_ability_and_effect_keywords, english_keyword_array, language_keyword_array)

            english_card_granted_keywords = english_card['granted_keywords']
            card_object['granted_keywords'] = convert_english_keywords_to_language.convert_english_keywords_to_language(language, english_card_granted_keywords, english_keyword_array, language_keyword_array)

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

            card_object['played_horizontally'] = english_card['played_horizontally']
            card_object['blitz_legal'] = english_card['blitz_legal']
            card_object['cc_legal'] = english_card['cc_legal']
            card_object['commoner_legal'] = english_card['commoner_legal']

            card_object['blitz_living_legend'] = english_card['blitz_living_legend']
            if 'blitz_living_legend_start' in english_card:
                card_object['blitz_living_legend_start'] = english_card['blitz_living_legend_start']

            card_object['cc_living_legend'] = english_card['cc_living_legend']
            if 'cc_living_legend_start' in english_card:
                card_object['cc_living_legend_start'] = english_card['cc_living_legend_start']

            card_object['blitz_banned'] = english_card['blitz_banned']
            if 'blitz_banned_start' in english_card:
                card_object['blitz_banned_start'] = english_card['blitz_banned_start']

            card_object['cc_banned'] = english_card['cc_banned']
            if 'cc_banned_start' in english_card:
                card_object['cc_banned_start'] = english_card['cc_banned_start']

            card_object['commoner_banned'] = english_card['commoner_banned']
            if 'commoner_banned_start' in english_card:
                card_object['commoner_banned_start'] = english_card['commoner_banned_start']

            card_object['upf_banned'] = english_card['upf_banned']
            if 'upf_banned_start' in english_card:
                card_object['upf_banned_start'] = english_card['upf_banned_start']

            card_object['blitz_suspended'] = english_card['blitz_suspended']
            if 'blitz_suspended_start' in english_card:
                card_object['blitz_suspended_start'] = english_card['blitz_suspended_start']
            if 'blitz_suspended_end' in english_card:
                card_object['blitz_suspended_end'] = english_card['blitz_suspended_end']

            card_object['cc_suspended'] = english_card['cc_suspended']
            if 'cc_suspended_start' in english_card:
                card_object['cc_suspended_start'] = english_card['cc_suspended_start']
            if 'cc_suspended_end' in english_card:
                card_object['cc_suspended_end'] = english_card['cc_suspended_end']

            card_object['commoner_suspended'] = english_card['commoner_suspended']
            if 'commoner_suspended_start' in english_card:
                card_object['commoner_suspended_start'] = english_card['commoner_suspended_start']
            if 'commoner_suspended_end' in english_card:
                card_object['commoner_suspended_end'] = english_card['commoner_suspended_end']

            variations = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            variation_unique_ids = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            image_urls = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            # Clean up fields

            card_object['functional_text'] = card_object['functional_text'].replace("'", "''")
            card_object['functional_text_plain'] = card_object['functional_text_plain'].replace("'", "''")
            card_object['flavor_text'] = card_object['flavor_text'].replace("'", "''")
            card_object['flavor_text_plain'] = card_object['flavor_text_plain'].replace("'", "''")


            # Card Printings

            card_printing_array = []

            has_different_artists = len(artists) > 1
            artists_switched_mid_print = len([x for x in artists if " — " in x or " – " in x or " - " in x]) > 0
            rarities_switched_mid_print = len([x for x in rarities if " — " in x or " – " in x or " - " in x]) > 0

            for variation_index, variation in enumerate(variations):
                card_variation = {}

                variation_split = re.split("— | – | - ", variation.strip())
                image_url_data = [helper_functions.convert_image_data(x) for x in image_urls]
                unique_id_data = [helper_functions.convert_variation_unique_id_data(x) for x in variation_unique_ids]

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
                card_variation['set_unique_id'] = helper_functions.get_set_unique_id(set_id, language, language_set_array, set_unique_id_cache)
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

    with language_card_json_path.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {language} card.csv\n")