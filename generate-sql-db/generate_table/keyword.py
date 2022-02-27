import csv
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE keywords (
            keyword VARCHAR(255) PRIMARY KEY,
            description VARCHAR(1000) NOT NULL
        )
        """

    try:
        print("Creating keywords table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS keywords
        """

    try:
        print("Dropping keywords table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert(cur, keyword, name):
    sql = """INSERT INTO keywords(keyword, description)
             VALUES(%s, %s) RETURNING keyword;"""
    try:
        print("Inserting {} keyword...".format(keyword))

        # execute the INSERT statement
        cur.execute(sql, (keyword,name))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out keywords table from keyword.csv...\n")

    path = Path(__file__).parent / "../../csvs/keyword.csv"
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            keyword = row[0]
            description = row[1]
            insert(cur, keyword, description)
            print(', '.join(row))

        print("\nSuccessfully filled keywords table\n")