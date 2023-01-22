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
        exit()

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
        exit()

def insert(cur, name):
    def check_if_artist_exists():
        select_sql = """SELECT name FROM artists WHERE name = %s;"""
        select_data = (name,)

        try:
            cur.execute(select_sql, select_data)
            selected_data = cur.fetchone()

            return selected_data is not None
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            exit()

    if check_if_artist_exists():
        print(f"Artist {name} already exists, skipping")
        return

    sql = """INSERT INTO artists(name)
             VALUES(%s) RETURNING name;"""
    data = (name,)

    try:
        print("Inserting {} artist...".format(name))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur, language):
    print(f"Filling out artists table from {language} artist.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/artist.json"
    with path.open(newline='') as jsonfile:
        artist_array = json.load(jsonfile)

        for artist in artist_array:
            name = artist['name']

            insert(cur, name)

        print(f"\nSuccessfully filled artists table with {language} data\n")