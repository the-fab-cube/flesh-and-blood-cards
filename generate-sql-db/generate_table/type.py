import csv
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
    print("Filling out types table from type.csv...\n")

    path = Path(__file__).parent / "../../csvs/type.csv"
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            name = row[0]
            insert(cur, name)
            # print(', '.join(row))

        print("\nSuccessfully filled types table\n")