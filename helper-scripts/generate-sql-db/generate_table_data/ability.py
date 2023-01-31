import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE abilities (
            unique_id VARCHAR(21) NOT NULL,
            name VARCHAR(255) NOT NULL,
            PRIMARY KEY (unique_id)
        )
        """

    try:
        print("Creating abilities table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS abilities
        """

    try:
        print("Dropping abilities table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def insert(cur, unique_id, name):
    sql = """INSERT INTO abilities(unique_id, name)
        VALUES(%s, %s) RETURNING name;"""
    data = (unique_id, name)
    try:
        print("Inserting {} ability...".format(name))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur):
    print("Filling out abilities table from ability.json...\n")

    path = Path(__file__).parent / "../../../json/english/ability.json"
    with path.open(newline='') as jsonfile:
        ability_array = json.load(jsonfile)

        for ability in ability_array:
            unique_id = ability['unique_id']
            name = ability['name']

            insert(cur, unique_id, name)

        print("\nSuccessfully filled abilities table\n")