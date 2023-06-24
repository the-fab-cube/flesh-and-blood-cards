import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

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
        exit()

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
        exit()

def prep_function(icon_entry, language):
    icon = icon_entry['icon']
    description = icon_entry['description']

    print("Prepping {} icon...".format(id))

    return (icon, description)

def upsert_function(cur, icons):
    print("Upserting {} icons".format(len(icons)))

    upsert_array(
        cur,
        "icons",
        icons,
        2,
        "(icon, description)",
        "(icon)",
        "UPDATE SET description = EXCLUDED.description"
    )

def generate_table_data(cur):
    print("Filling out icons table from icon.json...\n")

    path = Path(__file__).parent / "../../../json/english/icon.json"
    with path.open(newline='') as jsonfile:
        icon_array = json.load(jsonfile)

        prep_and_upsert_all(cur, icon_array, prep_function, upsert_function)

        print("\nSuccessfully filled icons table\n")