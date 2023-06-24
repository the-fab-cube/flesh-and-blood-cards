import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE type_translations (
            type_unique_id VARCHAR(21) NOT NULL,
            language VARCHAR(10) NOT NULL,
            name VARCHAR(255),
            FOREIGN KEY (type_unique_id) REFERENCES types (unique_id),
            PRIMARY KEY (type_unique_id, language)
        )
        """

    try:
        print("Creating type_translations table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS type_translations
        """

    try:
        print("Dropping type_translations table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def insert(cur, type_unique_id, language, name):
    sql = """INSERT INTO type_translations(type_unique_id, language, name)
             VALUES(%s, %s, %s) RETURNING name;"""
    data = (type_unique_id, language, name)

    try:
        print("Inserting {0} translation for type {1} ({2})...".format(
            language,
            type_unique_id,
            name
        ))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(type_entry, language):
    type_unique_id = type_entry['unique_id']
    name = type_entry['name']

    print("Prepping {0} translation for type {1} ({2})...".format(
        language,
        type_unique_id,
        name
    ))

    return (type_unique_id, language, name)

def upsert_function(cur, type_translations):
    print("Upserting {} type_translations".format(len(type_translations)))

    upsert_array(
        cur,
        "type_translations",
        type_translations,
        3,
        "(type_unique_id, language, name)",
        "(type_unique_id, language)",
        "UPDATE SET name = EXCLUDED.name "
    )

def generate_table_data(cur, language):
    print(f"Filling out type_translations table from {language} type.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/type.json"
    with path.open(newline='') as jsonfile:
        type_array = json.load(jsonfile)

        prep_and_upsert_all(cur, type_array, prep_function, upsert_function, language)

        print(f"\nSuccessfully filled type_translations table with {language} data\n")