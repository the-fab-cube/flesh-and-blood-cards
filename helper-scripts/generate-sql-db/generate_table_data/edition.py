import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE editions (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """

    try:
        print("Creating editions table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS editions
        """

    try:
        print("Dropping editions table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(edition, language):
    id = edition['id']
    name = edition['name']

    print("Prepping {} edition...".format(id))

    return (id, name)

def upsert_function(cur, editions):
    print("Upserting {} editions".format(len(editions)))

    upsert_array(
        cur,
        "editions",
        editions,
        2,
        "(id, name)",
        "(id)",
        "UPDATE SET name = EXCLUDED.name"
    )

def generate_table_data(cur):
    print("Filling out editions table from edition.json...\n")

    path = Path(__file__).parent / "../../../json/english/edition.json"
    with path.open(newline='') as jsonfile:
        edition_array = json.load(jsonfile)

        prep_and_upsert_all(cur, edition_array, prep_function, upsert_function)

        print("\nSuccessfully filled editions table\n")