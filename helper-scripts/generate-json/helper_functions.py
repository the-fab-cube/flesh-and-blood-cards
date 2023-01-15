import re

def convert_image_data(image_url):
    image_url_split = re.split("— | – | - ", image_url.strip())

    image_url_data = {}
    image_url_data['image_url'] = image_url_split[0]
    image_url_data['card_id'] = image_url_split[1]
    image_url_data['set_edition'] = image_url_split[2]
    image_url_data['alternate_art_type'] = None
    if len(image_url_split) >= 4:
        image_url_data['alternate_art_type'] = image_url_split[3]

    return image_url_data

def convert_to_array(field):
    return [convert_to_null(x) for x in field.split(", ") if x.strip() != ""]

def convert_to_null(field):
    if field.strip().lower() == "null":
        return None
    else:
        return field

def convert_variation_unique_id_data(variation_unique_id):
    variation_unique_id_split = re.split("— | – | - ", variation_unique_id.strip())

    variation_unique_id_data = {}
    variation_unique_id_data['unique_id'] = variation_unique_id_split[0]
    variation_unique_id_data['card_id'] = variation_unique_id_split[1]
    variation_unique_id_data['set_edition'] = variation_unique_id_split[2]
    variation_unique_id_data['alternate_art_type'] = None
    if len(variation_unique_id_split) >= 4:
        variation_unique_id_data['alternate_art_type'] = variation_unique_id_split[3]

    return variation_unique_id_data

def treat_blank_string_as_boolean(field, default_value=True):
    if field.strip() == '':
        return default_value

    return field

def treat_blank_string_as_none(field):
    if field == '':
        return None

    return field

def treat_string_as_boolean(field, default_value=True):
    return bool(treat_blank_string_as_boolean(field, default_value))