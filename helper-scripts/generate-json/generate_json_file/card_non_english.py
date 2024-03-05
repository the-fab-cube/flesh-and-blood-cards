import csv
import json
from pathlib import Path
from markdown_patch import unmark

import convert_english_abilities_to_language
import convert_english_keywords_to_language
import convert_english_types_to_language
import convert_card_printings_to_dict

def generate_json_file(language):
    print(f"Filling out {language} card.json from card.csv...")

    card_array = []

    english_json_path = Path(__file__).parent / "../../../json/english/card.json"
    english_ability_json_path = Path(__file__).parent / f"../../../json/english/ability.json"
    english_keyword_json_path = Path(__file__).parent / f"../../../json/english/keyword.json"
    english_type_json_path = Path(__file__).parent / f"../../../json/english/type.json"

    language_csv_path = Path(__file__).parent / f"../../../csvs/{language}/card.csv"
    language_card_printing_csv_path = Path(__file__).parent / f"../../../csvs/{language}/card-printing.csv"

    language_card_json_path = Path(__file__).parent / f"../../../json/{language}/card.json"
    language_ability_json_path = Path(__file__).parent / f"../../../json/{language}/ability.json"
    language_keyword_json_path = Path(__file__).parent / f"../../../json/{language}/keyword.json"
    language_set_json_path = Path(__file__).parent / f"../../../json/{language}/set.json"
    language_type_json_path = Path(__file__).parent / f"../../../json/{language}/type.json"

    card_printing_dict = convert_card_printings_to_dict.convert_card_printings_to_dict(language, language_card_printing_csv_path)

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
        language_type_array = json.load(language_type_json_file)

        reader = csv.DictReader(csv_file, delimiter='\t', quotechar='"')

        for row in reader:
            card_object = {}

            card_unique_id = row['Unique ID']
            card_object['unique_id'] = card_unique_id

            # assumes there is an english card - script will throw an exception otherwise
            english_card = [x for x in english_card_array if x['unique_id'] == card_unique_id][0]

            card_object['name'] = row['Name']

            card_object['pitch'] = english_card['pitch']
            card_object['cost'] = english_card['cost']
            card_object['power'] = english_card['power']
            card_object['defense'] = english_card['defense']
            card_object['health'] = english_card['health']
            card_object['intelligence'] = english_card['intelligence']

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

            english_card_removed_keywords = english_card['removed_keywords']
            card_object['removed_keywords'] = convert_english_keywords_to_language.convert_english_keywords_to_language(language, english_card_removed_keywords, english_keyword_array, language_keyword_array)

            english_card_interacts_with_keywords = english_card['interacts_with_keywords']
            card_object['interacts_with_keywords'] = convert_english_keywords_to_language.convert_english_keywords_to_language(language, english_card_interacts_with_keywords, english_keyword_array, language_keyword_array)

            card_object['functional_text'] = row['Functional Text']
            card_object['functional_text_plain'] = unmark(card_object['functional_text'])

            card_object['type_text'] = row['Type Text']

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

            card_object['ll_restricted'] = english_card['ll_restricted']
            if 'll_restricted_start' in english_card:
                card_object['ll_restricted_start'] = english_card['ll_restricted_start']

            # Clean up fields

            card_object['functional_text'] = card_object['functional_text'].replace("'", "''")
            card_object['functional_text_plain'] = card_object['functional_text_plain'].replace("'", "''")

            # Card Printings

            card_printing_array = card_printing_dict[card_unique_id]

            card_object['printings'] = card_printing_array

            card_array.append(card_object)

    json_object = json.dumps(card_array, indent=4, ensure_ascii=False)

    with language_card_json_path.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {language} card.csv\n")