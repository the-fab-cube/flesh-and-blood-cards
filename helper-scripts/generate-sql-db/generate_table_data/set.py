import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE sets (
            unique_id VARCHAR(21) NOT NULL,
            id VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            start_card_id VARCHAR(15) NOT NULL,
            end_card_id VARCHAR(15) NOT NULL,
            PRIMARY KEY (unique_id),
            UNIQUE (unique_id, id)
        )
        """

    try:
        print("Creating sets table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

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
        exit()

def insert(cur, unique_id, id, name, start_card_id, end_card_id):
    def check_if_set_exists():
        select_sql = """SELECT unique_id, start_card_id, end_card_id FROM sets WHERE unique_id = %s;"""
        select_data = (unique_id,)

        try:
            cur.execute(select_sql, select_data)
            selected_data = cur.fetchone()

            if selected_data is not None:
                # Verify there weren't data entry issues with the card ids across languages
                if selected_data[1] != start_card_id or selected_data[2] != end_card_id:
                    raise Exception(f"There was a mismatch of card id start/end numbers for set with unique_id {unique_id}: {selected_data[1]}/{selected_data[2]} vs {start_card_id}/{end_card_id}")

                return True

            return False
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            exit()

    if check_if_set_exists():
        print(f"Set {id} with unique_id {unique_id} already exists, skipping")
        return

    sql = """INSERT INTO sets(unique_id, id, name, start_card_id, end_card_id)
             VALUES(%s, %s, %s, %s, %s);"""
    data = (unique_id, id, name, start_card_id, end_card_id)

    try:
        print("Inserting {} set with unique ID {}...".format(id, unique_id))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def generate_table_data(cur, language):
    print(f"Filling out sets table from {language} set.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/set.json"
    with path.open(newline='') as jsonfile:
        set_array = json.load(jsonfile)

        for set in set_array:
            unique_id = set['unique_id']
            id = set['id']
            name = set['name']
            start_card_id = set['start_card_id']
            end_card_id = set['end_card_id']

            insert(cur, unique_id, id, name, start_card_id, end_card_id)

        print(f"\nSuccessfully filled sets table with {language} data\n")