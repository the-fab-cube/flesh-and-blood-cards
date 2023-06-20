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
            set_printing['initial_release_date'] = helper_functions.convert_to_null(row['Initial Release Date'])
            set_printing['out_of_print_date'] = helper_functions.convert_to_null(row['Out of Print Date'])
            set_printing['product_page'] = helper_functions.convert_to_null(row['Product Page'])
            set_printing['collectors_center'] = helper_functions.convert_to_null(row['Collector\'s Center'])
            set_printing['card_gallery'] = helper_functions.convert_to_null(row['Card Gallery'])

            if set_unique_id not in set_printing_dict:
                set_printing_dict[set_unique_id] = []

            set_printing_dict[set_unique_id].append(set_printing)

    return set_printing_dict