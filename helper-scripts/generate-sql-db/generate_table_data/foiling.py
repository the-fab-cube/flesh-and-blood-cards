import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE foilings (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """

    try:
        print("Creating foilings table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS foilings
        """

    try:
        print("Dropping foilings table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def insert(cur, id, name):
    sql = """INSERT INTO foilings(id, name)
             VALUES(%s, %s) RETURNING id;"""
    data = (id, name)

    try:
        print("Inserting {} foiling...".format(id))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(edition, language):
    id = edition['id']
    name = edition['name']

    print("Prepping {} foiling...".format(id))

    return (id, name)

def upsert_function(cur, foilings):
    print("Upserting {} foilings".format(len(foilings)))

    upsert_array(
        cur,
        "foilings",
        foilings,
        2,
        "(id, name)",
        "(id)",
        "UPDATE SET name = EXCLUDED.name"
    )

def generate_table_data(cur):
    print("Filling out foilings table from foiling.json...\n")

    path = Path(__file__).parent / "../../../json/english/foiling.json"
    with path.open(newline='') as jsonfile:
        foiling_array = json.load(jsonfile)

        prep_and_upsert_all(cur, foiling_array, prep_function, upsert_function)

        print("\nSuccessfully filled foilings table\n")