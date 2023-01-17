import re

import helper_functions

# Generalize all english card keyword text (ex: Opt 2 -> Opt X with stored data of 2 or Viserai Specialization -> Specialization with stored data of Viserai)
# ->
# Find unique_id of english card keywords
# ->
# Convert english card keyword data objects to use corresponding language keyword text
# ->
# Replace langauge keywords with 'X' with actual data (ex: 2, 4, X)

def convert_english_keywords_to_language(language, english_card_keywords, english_keywords, language_keywords):
    # print(english_card_keywords)
    generalized_english_keywords = list(map(generalize_english_card_keyword_text, english_card_keywords))
    # print(generalized_english_keywords)
    generalized_english_keywords_with_ids = list(map(lambda x: add_unique_id_to_generalized_card_keyword_data(x, english_keywords), generalized_english_keywords))
    # print(generalized_english_keywords_with_ids)
    generalized_non_english_keywords_with_ids = list(map(lambda x: replace_english_keyword_text_with_non_english_text(x, language_keywords), generalized_english_keywords_with_ids))
    # print(generalized_non_english_keywords_with_ids)
    mapped_keywords = list(map(lambda x: convert_generalized_keyword_data_to_language_text(language, x), generalized_non_english_keywords_with_ids))
    # print(mapped_keywords)

    return mapped_keywords

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
        hero_gender = helper_functions.get_hero_gender_identity(extracted_specialization_hero_data)
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