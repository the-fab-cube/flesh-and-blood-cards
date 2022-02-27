import csv
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE icons (
            icon VARCHAR(255) PRIMARY KEY,
            description VARCHAR(255) NOT NULL
        )
        """

    try:
        print("Creating icons table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS icons
        """

    try:
        print("Dropping icons table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert(cur, icon, name):
    sql = """INSERT INTO icons(icon, description)
             VALUES(%s, %s) RETURNING icon;"""
    try:
        print("Inserting {} icon...".format(icon))

        # execute the INSERT statement
        cur.execute(sql, (icon,name))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out icons table from icon.csv...\n")

    path = Path(__file__).parent / "../../csvs/icon.csv"
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            icon = row[0]
            description = row[1]
            insert(cur, icon, description)
            # print(', '.join(row))

        print("\nSuccessfully filled icons table\n")