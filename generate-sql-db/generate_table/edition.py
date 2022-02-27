import csv
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

def insert(cur, id, name):
    sql = """INSERT INTO editions(id, name)
             VALUES(%s, %s) RETURNING id;"""
    try:
        print("Inserting {} edition...".format(id))
        # execute the INSERT statement
        cur.execute(sql, (id,name))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out editions table from edition.csv...\n")

    path = Path(__file__).parent / "../../csvs/edition.csv"
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            id = row[0]
            name = row[1]
            insert(cur, id, name)
            print(', '.join(row))

        print("\nSuccessfully filled editions table\n")