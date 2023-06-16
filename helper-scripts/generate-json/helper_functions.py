import re

def convert_to_array(field):
    return [convert_to_null(x) for x in field.split(", ") if x.strip() != ""]

def convert_to_null(field):
    if field.strip().lower() == "null":
        return None
    else:
        return field

# Used for gendered language translations
def get_hero_gender_identity(hero):
    hero_gender_identity = {
        'Arakni': None,
        'Azalea': 'Female',
        'Benji': 'Male',
        'Boltyn': 'Male',
        'Bravo': 'Male',
        'Briar': 'Female',
        'Chane': 'Male',
        'Dash': 'Female',
        'Data Doll': 'Female',
        'Dorinthea': 'Female',
        'Dromai': 'Female',
        'Emperor': 'Male',
        'Fai': 'Male',
        'Genis': 'Male',
        'Ira': 'Female',
        'Iyslander': 'Female',
        'Kano': 'Male',
        'Kassai': 'Female',
        'Katsu': 'Male',
        'Kavdaen': 'Male',
        'Kayo': 'Male',
        'Levia': 'Female',
        'Lexi': 'Female',
        'Oldhim': 'Male',
        'Prism': 'Female',
        'Rhinar': 'Male',
        'Ruu\'di': 'Male',
        'Shiyana': 'Female',
        'Taipanis': 'Male',
        'Taylor': 'Female',
        'Valda': 'Female',
        'Viserai': 'Male',
        'Yoji': 'Male',
        'Yorick': 'Male',
    }

    try:
        return hero_gender_identity[hero]
    except:
        print(f"ERROR: The hero {hero}'s gender could not be found, please make sure they're in the get_hero_gender_identity function (Yes I know this sounds weird, it's used for language translations that are affected by gender)")
        exit()

def get_set_printing_unique_id(set_id, edition, language, language_set_array, set_printing_unique_id_cache):
    if (set_id, edition) in set_printing_unique_id_cache:
        return set_printing_unique_id_cache[(set_id, edition)]

    for set in language_set_array:
        for set_printing in set['printings']:
            if set['id'] == set_id and set_printing['edition'] == edition:
                unique_id = set_printing['unique_id']
                set_printing_unique_id_cache[(set_id, edition)] = unique_id
                return unique_id

    print(f"Could not find the set with id {set_id} and edition {edition} in the {language} set.json")
    exit()

def treat_blank_string_as_boolean(field, default_value=True):
    if field.strip() == '':
        return default_value

    return field

def treat_blank_string_as_none(field):
    if field == '':
        return None

    return field

def treat_string_as_boolean(field, default_value=True):
    if field == 'No':
        return False
    if field == 'Yes':
        return True

    return bool(treat_blank_string_as_boolean(field, default_value))