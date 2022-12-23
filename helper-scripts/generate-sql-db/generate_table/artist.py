import json
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
             VALUES(%s) RETURNING name;"""
    data = (name)

    try:
        print("Inserting {} artist...".format(name))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_table(cur):
    print("Filling out artists table from artist.json...\n")

    path = Path(__file__).parent / "../../../json/artist.json"
    with path.open(newline='') as jsonfile:
        artist_array = json.load(jsonfile)

        for artist in artist_array:
            name = artist['name']

            insert(cur, name)

        print("\nSuccessfully filled artists table\n")