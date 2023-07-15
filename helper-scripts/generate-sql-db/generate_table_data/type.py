import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE types (
            unique_id VARCHAR(21) NOT NULL,
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (unique_id)
        )
        """

    try:
        print("Creating types table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS types
        """

    try:
        print("Dropping types table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(type, language):
    unique_id = type['unique_id']
    name = type['name']

    print("Prepping {} type...".format(unique_id))

    return (unique_id, name)

def upsert_function(cur, types):
    print("Upserting {} types".format(len(types)))

    upsert_array(
        cur,
        "types",
        types,
        2,
        "(unique_id, name)",
        "(unique_id)",
        "UPDATE SET name = EXCLUDED.name"
    )

def generate_table_data(cur):
    print("Filling out types table from type.json...\n")

    path = Path(__file__).parent / "../../../json/english/type.json"
    with path.open(newline='') as jsonfile:
        type_array = json.load(jsonfile)

        prep_and_upsert_all(cur, type_array, prep_function, upsert_function)

        print("\nSuccessfully filled types table\n")