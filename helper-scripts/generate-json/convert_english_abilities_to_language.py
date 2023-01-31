# Find unique_id of english card abilities
# ->
# Convert english card ability data objects to use corresponding language ability text

def convert_english_abilities_to_language(language, english_card_abilities, english_abilities, language_abilities):
    # print(english_card_abilities)
    unique_ids = list(map(lambda ability: get_unique_id_by_ability(ability, english_abilities), english_card_abilities))
    # print(unique_ids)
    non_english_card_abilities = list(map(lambda unique_id: get_ability_text_by_unique_id(unique_id, language_abilities), unique_ids))
    # print(non_english_card_abilities)

    return non_english_card_abilities

def get_unique_id_by_ability(ability, all_ability_data):
    matched_ability_data = [ability_data for ability_data in all_ability_data if ability == ability_data['name']]

    if len(matched_ability_data) != 1:
        print(f"ERROR: Could not properly find the unique_id for the ability {ability}")
        exit()

    return matched_ability_data[0]['unique_id']

def get_ability_text_by_unique_id(unique_id, all_ability_data):
    matched_ability_data = [ability_data for ability_data in all_ability_data if unique_id == ability_data['unique_id']]

    if len(matched_ability_data) != 1:
        print(f"ERROR: Could not properly find the ability for the unique_id {unique_id}")
        exit()

    return matched_ability_data[0]['name']