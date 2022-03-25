import csv
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

def insert(cur, id, description):
    sql = """INSERT INTO rarities(id, description)
             VALUES(%s, %s) RETURNING id;"""
    try:
        print("Inserting {} rarity...".format(id))

        # execute the INSERT statement
        cur.execute(sql, (id,description))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out rarities table from rarity.csv...\n")

    path = Path(__file__).parent / "../../csvs/rarity.csv"
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            id = row[0]
            description = row[1]
            insert(cur, id, description)
            # print(', '.join(row))

        print("\nSuccessfully filled rarities table\n")