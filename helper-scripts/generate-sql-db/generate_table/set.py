import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE sets (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            start_card_id VARCHAR(15) NOT NULL,
            end_card_id VARCHAR(15) NOT NULL
        )
        """

    try:
        print("Creating sets table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS sets
        """

    try:
        print("Dropping sets table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert(cur, id, name, start_card_id, end_card_id):
    sql = """INSERT INTO sets(id, name, start_card_id, end_card_id)
             VALUES(%s, %s, %s, %s);"""
    data = (id, name, start_card_id, end_card_id)

    try:
        print("Inserting {} set...".format(id))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out sets table from set.json...\n")

    path = Path(__file__).parent / "../../../json/english/set.json"
    with path.open(newline='') as jsonfile:
        set_array = json.load(jsonfile)

        for set in set_array:
            id = set['id']
            name = set['name']
            start_card_id = set['start_card_id']
            end_card_id = set['end_card_id']

            insert(cur, id, name, start_card_id, end_card_id)

        print("\nSuccessfully filled sets table\n")