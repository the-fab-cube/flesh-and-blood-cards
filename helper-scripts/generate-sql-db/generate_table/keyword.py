import json
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
    data = (keyword, name)

    try:
        print("Inserting {} keyword...".format(keyword))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out keywords table from keyword.json...\n")

    path = Path(__file__).parent / "../../../json/english/keyword.json"
    with path.open(newline='') as jsonfile:
        keyword_array = json.load(jsonfile)

        for keyword_entry in keyword_array:
            keyword = keyword_entry['keyword']
            description = keyword_entry['description']

            insert(cur, keyword, description)

        print("\nSuccessfully filled keywords table\n")