import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE card_references (
            card_unique_id VARCHAR(21) NOT NULL,
            referenced_card_unique_id VARCHAR(21) NOT NULL,
            FOREIGN KEY (card_unique_id) REFERENCES cards (unique_id),
            FOREIGN KEY (referenced_card_unique_id) REFERENCES cards (unique_id),
            UNIQUE (card_unique_id, referenced_card_unique_id)
        )
        """

    try:
        print("Creating card_references table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS card_references
        """

    try:
        print("Dropping card_references table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(association, language):
    card_unique_id = association['card_unique_id']
    referenced_card_unique_id = association['referenced_card_unique_id']

    print("Prepping {0} --> {1} card reference...".format(
        card_unique_id,
        referenced_card_unique_id,
    ))

    return (card_unique_id, referenced_card_unique_id)

def upsert_function(cur, card_references):
    print("Upserting {} card_references".format(len(card_references)))

    upsert_array(
        cur,
        "card_references",
        card_references,
        2,
        "(card_unique_id, referenced_card_unique_id)",
        "(card_unique_id, referenced_card_unique_id)",
        "NOTHING"
    )

def generate_table_data(cur):
    print(f"Filling out card_references table from card-reference.json...\n")

    path = Path(__file__).parent / f"../../../json/english/card-reference.json"
    with path.open(newline='') as jsonfile:
        association_array = json.load(jsonfile)

        prep_and_upsert_all(cur, association_array, prep_function, upsert_function)

        print(f"\nSuccessfully filled card_references table with data\n")