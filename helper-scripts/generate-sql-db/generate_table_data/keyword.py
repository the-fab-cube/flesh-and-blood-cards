import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE keywords (
            unique_id VARCHAR(21) NOT NULL,
            name VARCHAR(255),
            description VARCHAR(1000) NOT NULL,
            PRIMARY KEY (unique_id),
            UNIQUE (name)
        )
        """

    try:
        print("Creating keywords table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS keywords
        """

    try:
        print("Dropping keywords table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(keyword_entry, language):
    unique_id = keyword_entry['unique_id']
    name = keyword_entry['name']
    description = keyword_entry['description']

    print("Prepping {} keyword...".format(name))

    return (unique_id, name, description)

def upsert_function(cur, keywords):
    print("Upserting {} keywords".format(len(keywords)))

    upsert_array(
        cur,
        "keywords",
        keywords,
        3,
        "(unique_id, name, description)",
        "(unique_id)",
        "UPDATE SET (name, description) = (EXCLUDED.name, EXCLUDED.description)"
    )

def generate_table_data(cur):
    print("Filling out keywords table from english keyword.json...\n")

    path = Path(__file__).parent / "../../../json/english/keyword.json"
    with path.open(newline='') as jsonfile:
        keyword_array = json.load(jsonfile)

        prep_and_upsert_all(cur, keyword_array, prep_function, upsert_function)

        print("\nSuccessfully filled keywords table\n")