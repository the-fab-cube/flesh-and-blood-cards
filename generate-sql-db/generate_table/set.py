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
            start_card_id VARCHAR(15) NOT NULL,
            end_card_id VARCHAR(15) NOT NULL,
            product_pages VARCHAR(1000)[] NOT NULL,
            collectors_center VARCHAR(1000)[] NOT NULL,
            card_galleries VARCHAR(1000)[] NOT NULL
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

def insert(cur, id, name, editions, initial_release_dates, out_of_print_dates, start_card_id, end_card_id, product_pages, collectors_center, card_galleries):
    sql = """INSERT INTO sets(id, name, editions, initial_release_dates, out_of_print_dates, start_card_id, end_card_id, product_pages, collectors_center, card_galleries)
             VALUES('{0}', '{1}', '{{{2}}}', '{{{3}}}', '{{{4}}}', '{5}', '{6}', '{{{7}}}', '{{{8}}}', '{{{9}}}');"""
    try:
        print("Inserting {} set...".format(id))

        # execute the INSERT statement
        cur.execute(sql.format(id, name, editions, initial_release_dates, out_of_print_dates, start_card_id, end_card_id, product_pages, collectors_center, card_galleries))
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
            start_card_id = row[5]
            end_card_id = row[6]
            product_pages = row[7]
            collectors_center = row[8]
            card_galleries = row[9]
            insert(cur, id, name, editions, initial_release_dates, out_of_print_dates, start_card_id, end_card_id, product_pages, collectors_center, card_galleries)
            # print(', '.join(row))

        print("\nSuccessfully filled sets table\n")