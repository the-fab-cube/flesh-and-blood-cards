import csv
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE artists (
            name VARCHAR(1000) NOT NULL
        )
        """

    try:
        print("Creating artists table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS artists
        """

    try:
        print("Dropping artists table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert(cur, name):
    sql = """INSERT INTO artists(name)
             VALUES('{0}') RETURNING name;""".format(name)
    try:
        print("Inserting {} artist...".format(name))

        # execute the INSERT statement
        cur.execute(sql, (name))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out artists table from artist.csv...\n")

    path = Path(__file__).parent / "../../../csvs/artist.csv"
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            name = row[0]
            insert(cur, name)
            # print(', '.join(row))

        print("\nSuccessfully filled artists table\n")