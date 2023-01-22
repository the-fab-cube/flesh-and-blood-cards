import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE types (
            unique_id VARCHAR(21) NOT NULL,
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (unique_id)
        )
        """

    try:
        print("Creating types table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

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
        exit()

def insert(cur, unique_id, name):
    sql = """INSERT INTO types(unique_id, name)
        VALUES(%s, %s) RETURNING name;"""
    data = (unique_id, name)
    try:
        print("Inserting {} type...".format(name))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur):
    print("Filling out types table from type.json...\n")

    path = Path(__file__).parent / "../../../json/english/type.json"
    with path.open(newline='') as jsonfile:
        type_array = json.load(jsonfile)

        for type in type_array:
            unique_id = type['unique_id']
            name = type['name']

            insert(cur, unique_id, name)

        print("\nSuccessfully filled types table\n")