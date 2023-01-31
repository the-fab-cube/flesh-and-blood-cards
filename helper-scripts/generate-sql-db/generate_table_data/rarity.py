import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE rarities (
            id VARCHAR(255) PRIMARY KEY,
            description VARCHAR(255) NOT NULL
        )
        """

    try:
        print("Creating rarities table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS rarities
        """

    try:
        print("Dropping rarities table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def insert(cur, id, description):
    sql = """INSERT INTO rarities(id, description)
             VALUES(%s, %s) RETURNING id;"""
    data = (id, description)

    try:
        print("Inserting {} rarity...".format(id))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur):
    print("Filling out rarities table from rarity.json...\n")

    path = Path(__file__).parent / "../../../json/english/rarity.json"
    with path.open(newline='') as jsonfile:
        rarity_array = json.load(jsonfile)

        for rarity in rarity_array:
            id = rarity['id']
            description = rarity['description']

            insert(cur, id, description)

        print("\nSuccessfully filled rarities table\n")