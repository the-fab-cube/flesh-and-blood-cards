import csv
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE sets (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            editions VARCHAR(255)[] NOT NULL,
            initial_release_dates TIMESTAMP[] NOT NULL,
            out_of_print_dates TIMESTAMP[] NOT NULL,
            product_sites VARCHAR(1000)[] NOT NULL
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

def insert(cur, id, name, editions, initial_release_dates, out_of_print_dates, product_sites):
    sql = """INSERT INTO sets(id, name, editions, initial_release_dates, out_of_print_dates, product_sites)
             VALUES('{0}', '{1}', '{{{2}}}', '{{{3}}}', '{{{4}}}', '{{{5}}}');"""
    try:
        print("Inserting {} set...".format(id))

        # execute the INSERT statement
        cur.execute(sql.format(id, name, editions, initial_release_dates, out_of_print_dates, product_sites))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out sets table from set.csv...\n")

    path = Path(__file__).parent / "../../csvs/set.csv"
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            id = row[0]
            name = row[1]
            editions = row[2]
            initial_release_dates = row[3]
            out_of_print_dates = row[4]
            product_sites = row[5]
            insert(cur, id, name, editions, initial_release_dates, out_of_print_dates, product_sites)
            # print(', '.join(row))

        print("\nSuccessfully filled sets table\n")