import json
import psycopg2
from pathlib import Path

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

def insert(cur, card_unique_id, referenced_card_unique_id):
    sql = """INSERT INTO card_references(card_unique_id, referenced_card_unique_id)
            VALUES(%s, %s);"""
    data = (card_unique_id, referenced_card_unique_id)

    try:
        print("Inserting {0} --> {1} card reference...".format(
            card_unique_id,
            referenced_card_unique_id,
        ))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()
        raise error

def generate_table_data(cur):
    print(f"Filling out card_references table from card-reference.json...\n")

    path = Path(__file__).parent / f"../../../json/english/card-reference.json"
    with path.open(newline='') as jsonfile:
        association_array = json.load(jsonfile)

        for association in association_array:
            card_unique_id = association['card_unique_id']
            referenced_card_unique_id = association['referenced_card_unique_id']

            insert(cur, card_unique_id, referenced_card_unique_id)

        print(f"\nSuccessfully filled cards table with data\n")