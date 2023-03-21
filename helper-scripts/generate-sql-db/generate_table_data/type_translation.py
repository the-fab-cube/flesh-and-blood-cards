import json
import psycopg2
from pathlib import Path

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

def generate_table_data(cur, language):
    print(f"Filling out type_translations table from {language} type.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/type.json"
    with path.open(newline='') as jsonfile:
        type_array = json.load(jsonfile)

        for type_entry in type_array:
            unique_id = type_entry['unique_id']
            name = type_entry['name']

            insert(cur, unique_id, language, name)

        print(f"\nSuccessfully filled type_translations table with {language} data\n")