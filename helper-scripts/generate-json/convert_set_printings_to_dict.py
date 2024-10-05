import csv

import helper_functions

def convert_set_printings_to_dict(set_printing_csv_path):
    # index is the card unique id
    set_printing_dict = {}

    with (
        set_printing_csv_path.open(newline='') as csvfile,
    ):
        reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')

        for row in reader:
            set_printing = {}

            printing_unique_id = row['Unique ID']
            set_unique_id = row['Set Unique ID']

            set_printing['unique_id'] = printing_unique_id
            set_printing['edition'] = row['Edition']
            set_printing['start_card_id'] = row['Start Card Id']
            set_printing['end_card_id'] = row['End Card Id']
            set_printing['initial_release_date'] = helper_functions.treat_blank_string_as_none(row['Initial Release Date'])
            set_printing['out_of_print'] = helper_functions.treat_string_as_boolean(row['Out of Print'], default_value=False)
            set_printing['card_database'] = helper_functions.treat_blank_string_as_none(row['Card Database'])
            set_printing['product_page'] = helper_functions.treat_blank_string_as_none(row['Product Page'])
            set_printing['collectors_center'] = helper_functions.treat_blank_string_as_none(row['Collector\'s Center'])
            set_printing['card_gallery'] = helper_functions.treat_blank_string_as_none(row['Card Gallery'])
            set_printing['release_notes'] = helper_functions.treat_blank_string_as_none(row['Release Notes'])
            set_printing['set_logo'] = helper_functions.treat_blank_string_as_none(row['Set Logo'])

            if set_unique_id not in set_printing_dict:
                set_printing_dict[set_unique_id] = []

            set_printing_dict[set_unique_id].append(set_printing)

    return set_printing_dict