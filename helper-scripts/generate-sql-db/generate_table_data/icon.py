import json
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

def insert(cur, icon, description):
    sql = """INSERT INTO icons(icon, description)
             VALUES(%s, %s) RETURNING icon;"""
    data = (icon, description)

    try:
        print("Inserting {} icon...".format(icon))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur):
    print("Filling out icons table from icon.json...\n")

    path = Path(__file__).parent / "../../../json/english/icon.json"
    with path.open(newline='') as jsonfile:
        icon_array = json.load(jsonfile)

        for icon_entry in icon_array:
            icon = icon_entry['icon']
            description = icon_entry['description']

            insert(cur, icon, description)

        print("\nSuccessfully filled icons table\n")