import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE abilities (
            unique_id VARCHAR(21) NOT NULL,
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (unique_id)
        )
        """

    try:
        print("Creating abilities table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS abilities
        """

    try:
        print("Dropping abilities table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(ability, language):
        unique_id = ability['unique_id']
        name = ability['name']

        print("Prepping {} ability for upsert...".format(name))

        return (unique_id, name)

def upsert_function(cur, abilities):
        print("Upserting {} abilities".format(len(abilities)))

        upsert_array(
            cur,
            "abilities",
            abilities,
            2,
            "(unique_id, name)",
            "(unique_id)",
            "UPDATE SET name = EXCLUDED.name"
        )

def generate_table_data(cur):
    print("Filling out abilities table from ability.json...\n")

    path = Path(__file__).parent / "../../../json/english/ability.json"
    with path.open(newline='') as jsonfile:
        ability_array = json.load(jsonfile)

        prep_and_upsert_all(cur, ability_array, prep_function, upsert_function)

        print("\nSuccessfully filled abilities table\n")