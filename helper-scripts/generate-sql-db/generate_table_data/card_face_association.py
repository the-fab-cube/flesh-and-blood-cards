import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE card_face_associations (
            front_unique_id VARCHAR(21) NOT NULL,
            back_unique_id VARCHAR(21) NOT NULL,
            is_DFC BOOLEAN NOT NULL,
            FOREIGN KEY (front_unique_id) REFERENCES card_printings (unique_id),
            FOREIGN KEY (back_unique_id) REFERENCES card_printings (unique_id),
            UNIQUE (front_unique_id, back_unique_id)
        )
        """

    try:
        print("Creating card_face_associations table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS card_face_associations
        """

    try:
        print("Dropping card_face_associations table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def insert(cur, front_unique_id, back_unique_id, is_DFC):
    sql = """INSERT INTO card_face_associations(front_unique_id, back_unique_id, is_DFC)
            VALUES(%s, %s, %s);"""
    data = (front_unique_id, back_unique_id, is_DFC)

    try:
        print("Inserting {0} - {1} double-sided card association...".format(
            front_unique_id,
            back_unique_id
        ))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()
        raise error

def generate_table_data(cur, language):
    print(f"Filling out card_face_associations table from {language} card-face-association.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/card-face-association.json"
    with path.open(newline='') as jsonfile:
        association_array = json.load(jsonfile)

        for association in association_array:
            front_unique_id = association['front_unique_id']
            back_unique_id = association['back_unique_id']
            is_DFC = association['is_DFC']

            insert(cur, front_unique_id, back_unique_id, is_DFC)

        print(f"\nSuccessfully filled cards table with {language} data\n")