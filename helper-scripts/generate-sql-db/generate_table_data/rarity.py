import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE rarities (
            id VARCHAR(255) PRIMARY KEY,
            description VARCHAR(255) NOT NULL
        )
        """

    try:
        print("Creating rarities table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS rarities
        """

    try:
        print("Dropping rarities table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(rarity, language):
    id = rarity['id']
    description = rarity['description']

    print("Prepping {} rarity...".format(id))

    return (id, description)

def upsert_function(cur, rarities):
    print("Upserting {} rarities".format(len(rarities)))

    upsert_array(
        cur,
        "rarities",
        rarities,
        2,
        "(id, description)",
        "(id)",
        "UPDATE SET description = EXCLUDED.description"
    )

def generate_table_data(cur):
    print("Filling out rarities table from rarity.json...\n")

    path = Path(__file__).parent / "../../../json/english/rarity.json"
    with path.open(newline='') as jsonfile:
        rarity_array = json.load(jsonfile)

        prep_and_upsert_all(cur, rarity_array, prep_function, upsert_function)

        print("\nSuccessfully filled rarities table\n")