import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE set_editions (
            id VARCHAR(255) NOT NULL,
            edition VARCHAR(255) NOT NULL,
            initial_release_date TIMESTAMP,
            out_of_print_date TIMESTAMP,
            product_page VARCHAR(1000),
            collectors_center VARCHAR(1000),
            card_gallery VARCHAR(1000),
            FOREIGN KEY (id) REFERENCES sets (id),
            PRIMARY KEY (id, edition)
        )
        """

    try:
        print("Creating set_editions table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

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

def insert(cur, id, edition, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery):
    sql = """INSERT INTO set_editions(id, edition, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery)
             VALUES(%s, %s, %s, %s, %s, %s, %s);"""
    data = (id, edition, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery)

    try:
        print("Inserting {0} printing for set {1}...".format(
            edition,
            id
        ))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out set_editions table from set.json...\n")

    path = Path(__file__).parent / "../../../json/set.json"
    with path.open(newline='') as jsonfile:
        set_array = json.load(jsonfile)

        for set in set_array:
            id = set['id']

            for edition_entry in set['editions']:
                edition = edition_entry['edition']
                initial_release_date = edition_entry['initial_release_date'] #.lower().replace("null", "infinity") # Uses infinity instead of null because some parsers break parsing timestamp arrays with null
                out_of_print_date = edition_entry['out_of_print_date'] #.lower().replace("null", "infinity") # Uses infinity instead of null because some parsers break parsing timestamp arrays with null
                product_page = edition_entry['product_page']
                collectors_center = edition_entry['collectors_center']
                card_gallery = edition_entry['card_gallery']

                insert(cur, id, edition, initial_release_date, out_of_print_date, product_page, collectors_center, card_gallery)

        print("\nSuccessfully filled set_editions table\n")