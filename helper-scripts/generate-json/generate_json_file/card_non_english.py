import csv
import json
import re
from pathlib import Path
from markdown_patch import unmark

import helper_functions

# Generalize all english card keyword text (ex: Opt 2 -> Opt X with stored data of 2)
# ->
# Find unique_id of english card keywords
# ->
# Convert english card keyword data objects to use corresponding language keyword text
# ->
# Replace langauge keywords with 'X' with actual data (ex: 2, 4, X)

def get_hero_gender(hero):
    return "Male"

def get_keyword_text_by_unique_id(unique_id, all_keyword_data):
    matched_keyword_data = [keyword_data for keyword_data in all_keyword_data if unique_id == keyword_data['unique_id']]

    if len(matched_keyword_data) != 1:
        print(f"ERROR: Could not properly find the keyword for the unique_id {unique_id}")
        exit()

    return matched_keyword_data[0]['keyword']

def generalize_english_card_keyword_text(card_keyword):
    # Find number/X data
    card_matches_x_format = re.match("^([\D]*?)([\d| X]*)$", card_keyword)

    if card_matches_x_format is None:
        print("ERROR: Could not properly extract English keyword number/X data")
        exit()

    x_format_groups = card_matches_x_format.groups()
    keyword = x_format_groups[0].strip()
    extracted_x_data = x_format_groups[1].strip() if x_format_groups[1] != '' else None
    extracted_specialization_hero_data = None

    if extracted_x_data is not None:
        keyword += " X"

    # Find specialization hero data
    card_matches_specialization_format = re.match("^([\D]*?) (Specialization)$", keyword)

    if card_matches_specialization_format is not None:
        specialization_format_groups = card_matches_specialization_format.groups()
        extracted_specialization_hero_data = specialization_format_groups[0].strip()
        keyword = specialization_format_groups[1].strip()

    generalized_data = {
        'keyword': keyword,
        'extracted_x_data': extracted_x_data,
        'extracted_specialization_hero_data': extracted_specialization_hero_data
    }

    return generalized_data

def add_unique_id_to_generalized_card_keyword_data(generalized_card_keyword_data, all_keyword_data):
    matched_keyword_data = [keyword_data for keyword_data in all_keyword_data if generalized_card_keyword_data['keyword'] == keyword_data['keyword']]

    if len(matched_keyword_data) != 1:
        print(f"ERROR: Could not properly find the unique_id for the keyword {generalized_card_keyword_data['keyword']}")
        exit()

    generalized_data = {
        'unique_id': matched_keyword_data[0]['unique_id'],
        'keyword': generalized_card_keyword_data['keyword'],
        'extracted_x_data': generalized_card_keyword_data['extracted_x_data'],
        'extracted_specialization_hero_data': generalized_card_keyword_data['extracted_specialization_hero_data']
    }

    return generalized_data

def replace_english_keyword_text_with_non_english_text(generalized_card_keyword_data, all_non_english_keyword_data):
    non_english_keyword_text = get_keyword_text_by_unique_id(generalized_card_keyword_data['unique_id'], all_non_english_keyword_data)

    generalized_card_keyword_data['keyword'] = non_english_keyword_text

    return generalized_card_keyword_data

def convert_generalized_keyword_data_to_language_text(language, generalized_card_keyword_data):
    # Extracts matching groups from keyword with format, matching only if the string " X" is in it:
    # 0 - keyword portion before " X"
    # 1 - the string " X" if it is in the keyword
    # 2 - keyword portion after the X, if any
    #
    # Note: If this does not match, just use the full keyword to start
    card_matches_x_format = re.match("^(\D*?)( X)( \D*)?$", generalized_card_keyword_data['keyword'])

    keyword_base = generalized_card_keyword_data['keyword']
    keyword_extra = None

    if card_matches_x_format is not None:
        x_format_groups = card_matches_x_format.groups()
        print(x_format_groups)
        keyword_base = x_format_groups[0].strip()
        keyword_extra = x_format_groups[2].strip() if x_format_groups[2] is not None else None

    extracted_x_data = generalized_card_keyword_data['extracted_x_data']
    extracted_specialization_hero_data = generalized_card_keyword_data['extracted_specialization_hero_data']

    # Compile keyword
    keyword = keyword_base

    if extracted_x_data is not None:
        keyword += f" {extracted_x_data}"
        if keyword_extra is not None:
            keyword += f" {keyword_extra}"

    if extracted_specialization_hero_data is not None:
        hero_gender = get_hero_gender(extracted_specialization_hero_data)
        match language:
            case "english":
                keyword = f"{extracted_specialization_hero_data} {keyword}"
            case "french":
                if hero_gender == "Male":
                    keyword += f" de {extracted_specialization_hero_data}"
                elif hero_gender == "Female":
                    keyword += f" d'{extracted_specialization_hero_data}"
                else:
                    keyword += f" de {extracted_specialization_hero_data}" # TODO: Check if this is right
            case "german":
                keyword = f"{extracted_specialization_hero_data}-{keyword}"
            case "italian":
                keyword = f"{keyword} di {extracted_specialization_hero_data}"
            case "spanish":
                keyword = f"{keyword} de {extracted_specialization_hero_data}"
            case _:
                print(f"ERROR: Cannot currently handle keyword specialization formatting for {language}")
                exit()

    return keyword


def convert_english_keywords_to_language(language, english_card_keywords, english_keywords, language_keywords):
    print(english_card_keywords)
    generalized_english_keywords = list(map(generalize_english_card_keyword_text, english_card_keywords))
    print(generalized_english_keywords)
    generalized_english_keywords_with_ids = list(map(lambda x: add_unique_id_to_generalized_card_keyword_data(x, english_keywords), generalized_english_keywords))
    print(generalized_english_keywords_with_ids)
    generalized_non_english_keywords_with_ids = list(map(lambda x: replace_english_keyword_text_with_non_english_text(x, language_keywords), generalized_english_keywords_with_ids))
    print(generalized_non_english_keywords_with_ids)
    mapped_keywords = list(map(lambda x: convert_generalized_keyword_data_to_language_text(language, x), generalized_non_english_keywords_with_ids))
    print(mapped_keywords)

    return mapped_keywords

def generate_json_file(language):
    print(f"Filling out {language} card.json from card.csv...")

    card_array = []

    english_json_path = Path(__file__).parent / "../../../json/english/card.json"
    english_keyword_json_path = Path(__file__).parent / f"../../../json/english/keyword.json"
    csv_path = Path(__file__).parent / f"../../../csvs/{language}/card.csv"
    card_json_path = Path(__file__).parent / f"../../../json/{language}/card.json"
    language_keyword_json_path = Path(__file__).parent / f"../../../json/{language}/keyword.json"

    with csv_path.open(newline='') as csv_file, english_json_path.open(newline='') as english_card_json_file, english_keyword_json_path.open(newline='') as english_keyword_json_file, language_keyword_json_path.open(newline='') as language_keyword_json_file:
        english_card_array = json.load(english_card_json_file)
        english_keyword_array = json.load(english_keyword_json_file)
        language_keyword_array = json.load(language_keyword_json_file)

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

            card_object['types'] = helper_functions.convert_to_array(row[rowId])
            rowId += 1

            english_card_keywords = english_card['card_keywords']
            card_object['card_keywords'] = convert_english_keywords_to_language(language, english_card_keywords, english_keyword_array, language_keyword_array)
            rowId += 1
            print("")

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

    with card_json_path.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {language} card.csv\n")