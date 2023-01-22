import json
import psycopg2
from pathlib import Path

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

def insert(cur, unique_id, name, description):
    sql = """INSERT INTO keywords(unique_id, name, description)
             VALUES(%s, %s, %s) RETURNING name;"""
    data = (unique_id, name, description)

    try:
        print("Inserting {} keyword...".format(name))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur):
    print("Filling out keywords table from english keyword.json...\n")

    path = Path(__file__).parent / "../../../json/english/keyword.json"
    with path.open(newline='') as jsonfile:
        keyword_array = json.load(jsonfile)

        for keyword_entry in keyword_array:
            unique_id = keyword_entry['unique_id']
            name = keyword_entry['name']
            description = keyword_entry['description']

            insert(cur, unique_id, name, description)

        print("\nSuccessfully filled keywords table\n")