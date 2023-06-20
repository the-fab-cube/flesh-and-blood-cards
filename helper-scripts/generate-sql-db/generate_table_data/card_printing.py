import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE card_printings (
            unique_id VARCHAR(21) NOT NULL,
            card_unique_id VARCHAR(21) NOT NULL,
            set_printing_unique_id VARCHAR(21) NOT NULL,
            card_id VARCHAR(15) NOT NULL COLLATE numeric,
            set_id VARCHAR(15) NOT NULL COLLATE numeric,
            edition VARCHAR(15) NOT NULL,
            foiling VARCHAR(15) NOT NULL,
            rarity VARCHAR(15) NOT NULL,
            artist VARCHAR(1000) NOT NULL,
            art_variation VARCHAR(15) NOT NULL,
            flavor_text VARCHAR(10000) NOT NULL,
            flavor_text_plain VARCHAR(10000) NOT NULL,
            image_url VARCHAR(1000) NOT NULL,
            tcgplayer_product_id VARCHAR(100) NOT NULL,
            tcgplayer_url VARCHAR(1000) NOT NULL,
            FOREIGN KEY (card_unique_id) REFERENCES cards (unique_id),
            FOREIGN KEY (set_printing_unique_id) REFERENCES set_printings (unique_id),
            PRIMARY KEY (unique_id),
            UNIQUE (unique_id, card_id, edition, art_variation)
        )
        """

    try:
        print("Creating card_printings table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

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
        exit()

def insert(cur, unique_id, card_unique_id, set_printing_unique_id, card_id, set_id, edition, foiling, rarity, artist,
            art_variation, flavor_text, flavor_text_plain, image_url, tcgplayer_product_id, tcgplayer_url):
    sql = """INSERT INTO card_printings(unique_id, card_unique_id, set_printing_unique_id, card_id, set_id, edition, foiling, rarity, artist,
                art_variation, flavor_text, flavor_text_plain, image_url, tcgplayer_product_id, tcgplayer_url)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    data = (unique_id, card_unique_id, set_printing_unique_id, card_id, set_id, edition, foiling, rarity, artist,
                art_variation, flavor_text, flavor_text_plain, image_url, tcgplayer_product_id, tcgplayer_url)

    try:
        print("Inserting {0} - {1} - {2} printing for card {3} ({4})...".format(
            edition,
            rarity,
            art_variation if art_variation != '' else 'null',
            card_id,
            card_unique_id
        ))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

# TODO: Add non-english cards
def generate_table_data(cur, url_for_images = None):
    print("Filling out card_printings table from english card.json...\n")

    path = Path(__file__).parent / "../../../json/english/card.json"
    with path.open(newline='') as jsonfile:
        card_array = json.load(jsonfile)

        for card in card_array:
            card_unique_id = card['unique_id']

            for printing in card['printings']:
                unique_id = printing['unique_id']
                set_printing_unique_id = printing['set_printing_unique_id']
                card_id = printing['id']
                set_id = printing['set_id']
                edition = printing['edition']
                foiling = printing['foiling']
                rarity = printing['rarity']
                artist = printing['artist']
                art_variation = printing['art_variation']
                flavor_text = printing['flavor_text']
                flavor_text_plain = printing['flavor_text_plain']
                image_url = printing['image_url']
                tcgplayer_product_id = ""
                tcgplayer_url = ""

                if 'tcgplayer_product_id' in printing:
                    tcgplayer_product_id = printing['tcgplayer_product_id']
                if 'tcgplayer_url' in printing:
                    tcgplayer_url = printing['tcgplayer_url']

                if url_for_images is not None and image_url is not None:
                    image_url = image_url.replace("https://storage.googleapis.com/fabmaster/media/images/", url_for_images)
                    image_url = image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/", url_for_images)
                    image_url = image_url.replace("https://dhhim4ltzu1pj.cloudfront.net/media/images/", url_for_images)

                if art_variation is None:
                    art_variation = ""
                if image_url is None:
                    image_url = ""

                insert(cur, unique_id, card_unique_id, set_printing_unique_id, card_id, set_id, edition, foiling, rarity, artist,
                        art_variation, flavor_text, flavor_text_plain, image_url, tcgplayer_product_id, tcgplayer_url)

        print("\nSuccessfully filled card_printings table\n")