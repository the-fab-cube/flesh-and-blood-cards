import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE set_printings (
            unique_id VARCHAR(21) NOT NULL,
            set_unique_id VARCHAR(21) NOT NULL,
            language VARCHAR(10) NOT NULL,
            edition VARCHAR(255) NOT NULL,
            start_card_id VARCHAR(15) NOT NULL,
            end_card_id VARCHAR(15) NOT NULL,
            initial_release_date TIMESTAMP,
            out_of_print_date TIMESTAMP,
            product_page VARCHAR(1000),
            collectors_center VARCHAR(1000),
            card_gallery VARCHAR(1000),
            FOREIGN KEY (set_unique_id) REFERENCES sets (unique_id),
            PRIMARY KEY (unique_id),
            UNIQUE (set_unique_id, language, edition)
        )
        """

    try:
        print("Creating set_printings table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS set_printings
        """

    try:
        print("Dropping set_printings table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(set_printing, language):
        set_unique_id = set_printing['set_unique_id']
        unique_id = set_printing['unique_id']
        edition = set_printing['edition']
        start_card_id = set_printing['start_card_id']
        end_card_id = set_printing['end_card_id']
        initial_release_date = set_printing['initial_release_date']
        out_of_print_date = set_printing['out_of_print_date']
        product_page = set_printing['product_page']
        collectors_center = set_printing['collectors_center']
        card_gallery = set_printing['card_gallery']

        print("Prepping {0} printing for {1} set {2}...".format(
            edition,
            language,
            unique_id
        ))

        return (unique_id, set_unique_id, language, edition, start_card_id, end_card_id, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery)

def upsert_function(cur, set_printings):
        print("Upserting {} set_printings".format(len(set_printings)))

        upsert_array(
            cur,
            "set_printings",
            set_printings,
            11,
            "(unique_id, set_unique_id, language, edition, start_card_id, end_card_id, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery)",
            "(set_unique_id, language, edition)",
            "UPDATE SET (unique_id, start_card_id, end_card_id, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery) = (EXCLUDED.unique_id, EXCLUDED.start_card_id, EXCLUDED.end_card_id, EXCLUDED.initial_release_date, EXCLUDED.out_of_print_date, EXCLUDED.product_page, EXCLUDED.collectors_center, EXCLUDED.card_gallery)"
        )

def generate_table_data(cur, language):
    print(f"Filling out set_printings table from {language} set.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/set.json"
    with path.open(newline='') as jsonfile:
        set_array = json.load(jsonfile)
        set_printing_array = []

        for set in set_array:
            for printing_entry in set['printings']:
                set_printing_data = {}
                set_printing_data['set_unique_id'] = set['unique_id']
                set_printing_data['unique_id'] = printing_entry['unique_id']
                set_printing_data['edition'] = printing_entry['edition']
                set_printing_data['start_card_id'] = printing_entry['start_card_id']
                set_printing_data['end_card_id'] = printing_entry['end_card_id']
                set_printing_data['initial_release_date'] = printing_entry['initial_release_date']
                set_printing_data['out_of_print_date'] = printing_entry['out_of_print_date']
                set_printing_data['product_page'] = printing_entry['product_page']
                set_printing_data['collectors_center'] = printing_entry['collectors_center']
                set_printing_data['card_gallery'] = printing_entry['card_gallery']

                set_printing_array.append(set_printing_data)

        prep_and_upsert_all(cur, set_printing_array, prep_function, upsert_function, language)

        print("\nSuccessfully filled set_printings table\n")