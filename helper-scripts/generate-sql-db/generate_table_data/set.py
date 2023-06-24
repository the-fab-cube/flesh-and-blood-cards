import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE sets (
            unique_id VARCHAR(21) NOT NULL,
            id VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (unique_id),
            UNIQUE (unique_id, id)
        )
        """

    try:
        print("Creating sets table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS sets
        """

    try:
        print("Dropping sets table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(set, language):
        unique_id = set['unique_id']
        id = set['id']
        name = set['name']

        print("Prepping {} set with unique ID {}...".format(id, unique_id))

        return (unique_id, id, name)

def upsert_function(cur, sets):
        print("Upserting {} sets".format(len(sets)))

        upsert_array(
            cur,
            "sets",
            sets,
            3,
            "(unique_id, id, name)",
            "(unique_id)",
            "UPDATE SET (id, name) = (EXCLUDED.id, EXCLUDED.name)"
        )

def generate_table_data(cur, language):
    print(f"Filling out sets table from {language} set.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/set.json"
    with path.open(newline='') as jsonfile:
        set_array = json.load(jsonfile)

        prep_and_upsert_all(cur, set_array, prep_function, upsert_function, language)

        print(f"\nSuccessfully filled sets table with {language} data\n")