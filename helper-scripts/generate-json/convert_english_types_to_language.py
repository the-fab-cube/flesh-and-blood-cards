# Find unique_id of english card types
# ->
# Convert english card type data objects to use corresponding language type text

def convert_english_types_to_language(language, english_card_types, english_types, language_types):
    # print(english_card_types)
    unique_ids = list(map(lambda type: get_unique_id_by_type(type, english_types), english_card_types))
    # print(unique_ids)
    non_english_card_types = list(map(lambda unique_id: get_type_text_by_unique_id(unique_id, language_types), unique_ids))
    # print(non_english_card_types)

    return non_english_card_types

def get_unique_id_by_type(type, all_type_data):
    matched_type_data = [type_data for type_data in all_type_data if type == type_data['name']]

    if len(matched_type_data) != 1:
        print(f"ERROR: Could not properly find the unique_id for the type {type}")
        exit()

    return matched_type_data[0]['unique_id']

def get_type_text_by_unique_id(unique_id, all_type_data):
    matched_type_data = [type_data for type_data in all_type_data if unique_id == type_data['unique_id']]

    if len(matched_type_data) != 1:
        print(f"ERROR: Could not properly find the type for the unique_id {unique_id}")
        exit()

    return matched_type_data[0]['name']