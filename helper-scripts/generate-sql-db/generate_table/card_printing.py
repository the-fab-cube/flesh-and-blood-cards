import json
import psycopg2
from pathlib import Path
from markdown_patch import unmark

def create_table(cur):
    command = """
        CREATE TABLE card_printings (
            id VARCHAR(15) NOT NULL COLLATE numeric,
            name VARCHAR(255) NOT NULL,
            pitch VARCHAR(10) COLLATE numeric NOT NULL,
            set_id VARCHAR(15) NOT NULL COLLATE numeric,
            edition VARCHAR(15) NOT NULL,
            foilings VARCHAR(15)[] NOT NULL,
            rarity VARCHAR(15) NOT NULL,
            artist VARCHAR(1000) NOT NULL,
            art_variation VARCHAR(15) NOT NULL,
            image_url VARCHAR(1000) NOT NULL,
            FOREIGN KEY (name, pitch) REFERENCES cards (name, pitch),
            PRIMARY KEY(id, name, pitch, edition, art_variation)
        )
        """

    try:
        print("Creating card_printings table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS card_printings
        """

    try:
        print("Dropping card_printings table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert(cur, id, name, pitch, set_id, edition, foilings, rarity, artist, art_variation, image_url):
    sql = """INSERT INTO card_printings(id, name, pitch, set_id, edition, foilings, rarity, artist, art_variation, image_url)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    data = (id, name, pitch, set_id, edition, foilings, rarity, artist, art_variation, image_url)

    try:
        print("Inserting {0} - {1} - {2} printing for card {3} ({4} - {5})...".format(
            edition,
            rarity,
            art_variation if art_variation != '' else 'null',
            id,
            name,
            pitch
        ))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error

def treat_blank_string_as_boolean(field, value=True):
    if field == '':
        return value

    return field

def treat_blank_string_as_none(field):
    if field == '':
        return 'NULL'

    return "'" + field + "'"

def generate_table(cur, url_for_images = None):
    print("Filling out cards table from card.json...\n")

    path = Path(__file__).parent / "../../../json/english/card.json"
    with path.open(newline='') as jsonfile:
        card_array = json.load(jsonfile)

        for card in card_array:
            name = card['name']
            pitch = card['pitch']

            for printing in card['printings']:
                id = printing['id']
                set_id = printing['set_id']
                edition = printing['edition']
                foilings = printing['foilings']
                rarity = printing['rarity']
                artist = printing['artist']
                art_variation = printing['art_variation']
                image_url = printing['image_url']

                if url_for_images is not None and image_url is not None:
                    image_url = image_url.replace("https://storage.googleapis.com/fabmaster/media/images/", url_for_images)
                    image_url = image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/", url_for_images)

                if art_variation is None:
                    art_variation = ""
                if image_url is None:
                    image_url = ""

                insert(cur, id, name, pitch, set_id, edition, foilings, rarity, artist, art_variation, image_url)

        print("\nSuccessfully filled cards table\n")