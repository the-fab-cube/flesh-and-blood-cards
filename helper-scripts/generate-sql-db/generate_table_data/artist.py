import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE artists (
            name VARCHAR(1000) NOT NULL,
            UNIQUE (name)
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

def prep_function(artist, language):
        name = artist['name']

        print("Prepping {} artist for upsert...".format(name))

        return (name,)

def upsert_function(cur, artists):
        print("Upserting {} artists".format(len(artists)))

        upsert_array(
            cur,
            "artists",
            artists,
            1,
            "(name)",
            "(name)",
            "NOTHING"
        )

def generate_table_data(cur, language):
    print(f"Filling out artists table from {language} artist.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/artist.json"
    with path.open(newline='') as jsonfile:
        artist_array = json.load(jsonfile)

        prep_and_upsert_all(cur, artist_array, prep_function, upsert_function, language)

        print(f"\nSuccessfully filled artists table with {language} data\n")