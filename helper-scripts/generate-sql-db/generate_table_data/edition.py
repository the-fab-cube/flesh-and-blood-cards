import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE editions (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """

    try:
        print("Creating editions table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS editions
        """

    try:
        print("Dropping editions table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def insert(cur, id, name):
    sql = """INSERT INTO editions(id, name)
             VALUES(%s, %s) RETURNING id;"""
    data = (id, name)

    try:
        print("Inserting {} edition...".format(id))
        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur):
    print("Filling out editions table from edition.json...\n")

    path = Path(__file__).parent / "../../../json/english/edition.json"
    with path.open(newline='') as jsonfile:
        edition_array = json.load(jsonfile)

        for edition in edition_array:
            id = edition['id']
            name = edition['name']

            insert(cur, id, name)

        print("\nSuccessfully filled editions table\n")