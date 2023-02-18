import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE keyword_translations (
            keyword_unique_id VARCHAR(21) NOT NULL,
            language VARCHAR(10) NOT NULL,
            name VARCHAR(255),
            description VARCHAR(1000) NOT NULL,
            FOREIGN KEY (keyword_unique_id) REFERENCES keywords (unique_id),
            PRIMARY KEY (keyword_unique_id, language)
        )
        """

    try:
        print("Creating keyword_translations table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS keyword_translations
        """

    try:
        print("Dropping keyword_translations table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def insert(cur, keyword_unique_id, language, name, description):
    sql = """INSERT INTO keyword_translations(keyword_unique_id, language, name, description)
            VALUES(%s, %s, %s, %s);"""
    data = (keyword_unique_id, language, name, description)

    try:
        print("Inserting {0} translation for keyword {1} ({2})...".format(
            language,
            keyword_unique_id,
            name
        ))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()
        raise error

def generate_table_data(cur, language):
    print(f"Filling out keywords table from {language} card.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/keyword.json"
    with path.open(newline='') as jsonfile:
        keyword_array = json.load(jsonfile)

        for keyword in keyword_array:
            keyword_unique_id = keyword['unique_id']
            name = keyword['name']
            description = keyword['description']

            insert(cur, keyword_unique_id, language, name, description)

        print(f"\nSuccessfully filled keywords table with {language} data\n")