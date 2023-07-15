import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE ability_translations (
            ability_unique_id VARCHAR(21) NOT NULL,
            language VARCHAR(10) NOT NULL,
            name VARCHAR(255),
            FOREIGN KEY (ability_unique_id) REFERENCES abilities (unique_id),
            PRIMARY KEY (ability_unique_id, language)
        )
        """

    try:
        print("Creating ability_translations table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS ability_translations
        """

    try:
        print("Dropping ability_translations table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(ability_entry, language):
        ability_unique_id = ability_entry['unique_id']
        name = ability_entry['name']

        print("Prepping {0} translation for ability {1} ({2}) for upsert...".format(
            language,
            ability_unique_id,
            name
        ))

        return (ability_unique_id, language, name)

def upsert_function(cur, abilities):
        print("Upserting {} ability translations".format(len(abilities)))

        upsert_array(
            cur,
            "ability_translations",
            abilities,
            3,
            "(ability_unique_id, language, name)",
            "(ability_unique_id, language)",
            "UPDATE SET name = EXCLUDED.name"
        )

def generate_table_data(cur, language):
    print(f"Filling out ability_translations table from {language} ability.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/ability.json"
    with path.open(newline='') as jsonfile:
        ability_array = json.load(jsonfile)

        prep_and_upsert_all(cur, ability_array, prep_function, upsert_function)

        print(f"\nSuccessfully filled ability_translations table with {language} data\n")