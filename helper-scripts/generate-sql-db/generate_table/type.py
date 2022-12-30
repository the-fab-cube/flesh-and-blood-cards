import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE types (
            name VARCHAR(255) PRIMARY KEY
        )
        """

    try:
        print("Creating types table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS types
        """

    try:
        print("Dropping types table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert(cur, name):
    sql = """INSERT INTO types(name) VALUES('{}');"""
    try:
        print("Inserting {} type...".format(name))

        # execute the INSERT statement
        cur.execute(sql.format(name))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out types table from type.json...\n")

    path = Path(__file__).parent / "../../../json/english/type.json"
    with path.open(newline='') as jsonfile:
        type_array = json.load(jsonfile)

        for type in type_array:
            name = type['name']

            insert(cur, name)

        print("\nSuccessfully filled types table\n")