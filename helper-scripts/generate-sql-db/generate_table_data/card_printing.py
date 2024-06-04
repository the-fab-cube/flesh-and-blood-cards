import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

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

def prep_function(card_printing, language):
    card_unique_id = card_printing['card_unique_id']
    unique_id = card_printing['unique_id']
    set_printing_unique_id = card_printing['set_printing_unique_id']
    card_id = card_printing['id']
    set_id = card_printing['set_id']
    edition = card_printing['edition']
    foiling = card_printing['foiling']
    rarity = card_printing['rarity']
    artist = card_printing['artist']
    art_variation = card_printing['art_variation']
    flavor_text = card_printing['flavor_text']
    flavor_text_plain = card_printing['flavor_text_plain']
    image_url = card_printing['image_url']
    tcgplayer_product_id = ""
    tcgplayer_url = ""

    if 'tcgplayer_product_id' in card_printing:
        tcgplayer_product_id = card_printing['tcgplayer_product_id']
    if 'tcgplayer_url' in card_printing:
        tcgplayer_url = card_printing['tcgplayer_url']

    if art_variation is None:
        art_variation = ""
    if image_url is None:
        image_url = ""

    print("Prepping {0} - {1} - {2} printing for card {3} ({4})...".format(
        edition,
        rarity,
        art_variation if art_variation != '' else 'null',
        card_id,
        card_unique_id
    ))

    return (unique_id, card_unique_id, set_printing_unique_id, card_id, set_id, edition, foiling, rarity, artist,
                art_variation, flavor_text, flavor_text_plain, image_url, tcgplayer_product_id, tcgplayer_url)

def upsert_function(cur, card_printings):
    print("Upserting {} card_printings".format(len(card_printings)))

    upsert_array(
        cur,
        "card_printings",
        card_printings,
        15,
        """(unique_id, card_unique_id, set_printing_unique_id, card_id, set_id, edition, foiling, rarity, artist,
            art_variation, flavor_text, flavor_text_plain, image_url, tcgplayer_product_id, tcgplayer_url)""",
        "(unique_id)",
        """UPDATE SET
            (card_unique_id, set_printing_unique_id, card_id, set_id, edition, foiling, rarity, artist,
                art_variation, flavor_text, flavor_text_plain, image_url, tcgplayer_product_id, tcgplayer_url) =
            (EXCLUDED.card_unique_id, EXCLUDED.set_printing_unique_id, EXCLUDED.card_id, EXCLUDED.set_id, EXCLUDED.edition, EXCLUDED.foiling, EXCLUDED.rarity, EXCLUDED.artist,
                EXCLUDED.art_variation, EXCLUDED.flavor_text, EXCLUDED.flavor_text_plain, EXCLUDED.image_url, EXCLUDED.tcgplayer_product_id, EXCLUDED.tcgplayer_url)"""
    )

# TODO: Add non-english cards
def generate_table_data(cur, url_for_images = None):
    print("Filling out card_printings table from english card.json...\n")

    path = Path(__file__).parent / "../../../json/english/card.json"
    with path.open(newline='') as jsonfile:
        card_array = json.load(jsonfile)
        card_printing_array = []

        for card in card_array:
            card_unique_id = card['unique_id']

            for printing in card['printings']:
                printing['card_unique_id'] = card_unique_id

                image_url = printing['image_url']
                if url_for_images is not None and image_url is not None:
                    image_url = image_url.replace("https://storage.googleapis.com/fabmaster/media/images/", url_for_images)
                    image_url = image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/", url_for_images)
                    image_url = image_url.replace("https://dhhim4ltzu1pj.cloudfront.net/media/images/", url_for_images)
                    image_url = image_url.replace("https://d2wlb52bya4y8z.cloudfront.net/media/cards/", url_for_images)
                printing['image_url'] = image_url

                card_printing_array.append(printing)

        prep_and_upsert_all(cur, card_printing_array, prep_function, upsert_function)

        print("\nSuccessfully filled card_printings table\n")