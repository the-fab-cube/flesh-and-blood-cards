import json
import psycopg2
from pathlib import Path

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

def insert(cur, ability_unique_id, language, name):
    sql = """INSERT INTO ability_translations(ability_unique_id, language, name)
             VALUES(%s, %s, %s) RETURNING name;"""
    data = (ability_unique_id, language, name)

    try:
        print("Inserting {0} translation for ability {1} ({2})...".format(
            language,
            ability_unique_id,
            name
        ))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur, language):
    print(f"Filling out ability_translations table from {language} ability.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/ability.json"
    with path.open(newline='') as jsonfile:
        ability_array = json.load(jsonfile)

        for ability_entry in ability_array:
            unique_id = ability_entry['unique_id']
            name = ability_entry['name']

            insert(cur, unique_id, language, name)

        print(f"\nSuccessfully filled ability_translations table with {language} data\n")