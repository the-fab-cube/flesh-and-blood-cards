import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE keywords (
            name VARCHAR(255) PRIMARY KEY,
            description VARCHAR(1000) NOT NULL
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

def insert(cur, name, description):
    sql = """INSERT INTO keywords(name, description)
             VALUES(%s, %s) RETURNING name;"""
    data = (name, description)

    try:
        print("Inserting {} keyword...".format(name))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur):
    print("Filling out keywords table from keyword.json...\n")

    path = Path(__file__).parent / "../../../json/english/keyword.json"
    with path.open(newline='') as jsonfile:
        keyword_array = json.load(jsonfile)

        for keyword_entry in keyword_array:
            name = keyword_entry['name']
            description = keyword_entry['description']

            insert(cur, name, description)

        print("\nSuccessfully filled keywords table\n")