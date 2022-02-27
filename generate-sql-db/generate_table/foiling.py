import csv
import psycopg2
from pathlib import Path

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

def insert(cur, id, name):
    sql = """INSERT INTO foilings(id, name)
             VALUES(%s, %s) RETURNING id;"""
    try:
        print("Inserting {} foiling...".format(id))

        # execute the INSERT statement
        cur.execute(sql, (id,name))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out foilings table from foiling.csv...\n")

    path = Path(__file__).parent / "../../csvs/foiling.csv"
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            id = row[0]
            name = row[1]
            insert(cur, id, name)
            print(', '.join(row))

        print("\nSuccessfully filled foilings table\n")