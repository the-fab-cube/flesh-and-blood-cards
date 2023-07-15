import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

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

def prep_function(association, language):
    front_unique_id = association['front_unique_id']
    back_unique_id = association['back_unique_id']
    is_DFC = association['is_DFC']

    print("Prepping {0} - {1} double-sided card association...".format(
            front_unique_id,
            back_unique_id
        ))

    return (front_unique_id, back_unique_id, is_DFC)

def upsert_function(cur, card_face_associations):
    print("Upserting {} card_face_associations".format(len(card_face_associations)))

    upsert_array(
        cur,
        "card_face_associations",
        card_face_associations,
        3,
        "(front_unique_id, back_unique_id, is_DFC)",
        "(front_unique_id, back_unique_id)",
        "UPDATE SET is_DFC = EXCLUDED.is_DFC"
    )

def generate_table_data(cur, language):
    print(f"Filling out card_face_associations table from {language} card-face-association.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/card-face-association.json"
    with path.open(newline='') as jsonfile:
        association_array = json.load(jsonfile)

        prep_and_upsert_all(cur, association_array, prep_function, upsert_function, language)

        print(f"\nSuccessfully filled card_face_associations table with {language} data\n")