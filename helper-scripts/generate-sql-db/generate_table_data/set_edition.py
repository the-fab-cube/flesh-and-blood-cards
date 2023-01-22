import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE set_editions (
            unique_id VARCHAR(21) NOT NULL,
            set_unique_id VARCHAR(21) NOT NULL,
            language VARCHAR(10) NOT NULL,
            edition VARCHAR(255) NOT NULL,
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
        print("Creating set_editions table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS set_editions
        """

    try:
        print("Dropping set_editions table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def insert(cur, unique_id, set_unique_id, language, edition, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery):
    sql = """INSERT INTO set_editions(unique_id, set_unique_id, language, edition, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    data = (unique_id, set_unique_id, language, edition, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery)

    try:
        print("Inserting {0} printing for {1} set {2}...".format(
            edition,
            language,
            unique_id
        ))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur, language):
    print(f"Filling out set_editions table from {language} set.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/set.json"
    with path.open(newline='') as jsonfile:
        set_array = json.load(jsonfile)

        for set in set_array:
            set_unique_id = set['unique_id']

            for edition_entry in set['editions']:
                unique_id = edition_entry['unique_id']
                edition = edition_entry['edition']
                initial_release_date = edition_entry['initial_release_date'] #.lower().replace("null", "infinity") # Uses infinity instead of null because some parsers break parsing timestamp arrays with null
                out_of_print_date = edition_entry['out_of_print_date'] #.lower().replace("null", "infinity") # Uses infinity instead of null because some parsers break parsing timestamp arrays with null
                product_page = edition_entry['product_page']
                collectors_center = edition_entry['collectors_center']
                card_gallery = edition_entry['card_gallery']

                insert(cur, unique_id, set_unique_id, language, edition, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery)

        print("\nSuccessfully filled set_editions table\n")