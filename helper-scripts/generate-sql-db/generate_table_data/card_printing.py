import json
import psycopg2
from pathlib import Path

from helpers import replace_image_url_domain, upsert_array, prep_and_upsert_all

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
            artists VARCHAR(1000) NOT NULL,
            art_variations VARCHAR(15) NOT NULL,
            expansion_slot BOOLEAN NOT NULL DEFAULT FALSE,
            flavor_text VARCHAR(10000) NOT NULL,
            flavor_text_plain VARCHAR(10000) NOT NULL,
            image_url VARCHAR(1000) NOT NULL,
            image_rotation_degrees smallint NOT NULL,
            tcgplayer_product_id VARCHAR(100) NOT NULL,
            tcgplayer_url VARCHAR(1000) NOT NULL,
            FOREIGN KEY (card_unique_id) REFERENCES cards (unique_id),
            FOREIGN KEY (set_printing_unique_id) REFERENCES set_printings (unique_id),
            PRIMARY KEY (unique_id),
            UNIQUE (unique_id, card_id, edition, art_variations)
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
    artists = card_printing['artists']
    art_variations = card_printing['art_variations']
    expansion_slot = card_printing['expansion_slot']
    flavor_text = card_printing['flavor_text']
    flavor_text_plain = card_printing['flavor_text_plain']
    image_url = card_printing['image_url']
    image_rotation_degrees = card_printing['image_rotation_degrees']
    tcgplayer_product_id = ""
    tcgplayer_url = ""

    if 'tcgplayer_product_id' in card_printing:
        tcgplayer_product_id = card_printing['tcgplayer_product_id']
    if 'tcgplayer_url' in card_printing:
        tcgplayer_url = card_printing['tcgplayer_url']

    if image_url is None:
        image_url = ""

    print("Prepping {0} - {1} - {2} printing for card {3} ({4})...".format(
        edition,
        rarity,
        art_variations,
        card_id,
        card_unique_id
    ))

    return (unique_id, card_unique_id, set_printing_unique_id, card_id, set_id, edition, foiling, rarity, artists,
                art_variations, expansion_slot, flavor_text, flavor_text_plain, image_url, image_rotation_degrees, tcgplayer_product_id, tcgplayer_url)

def upsert_function(cur, card_printings):
    print("Upserting {} card_printings".format(len(card_printings)))

    upsert_array(
        cur,
        "card_printings",
        card_printings,
        17,
        """(unique_id, card_unique_id, set_printing_unique_id, card_id, set_id, edition, foiling, rarity, artists,
            art_variations, expansion_slot, flavor_text, flavor_text_plain, image_url, image_rotation_degrees, tcgplayer_product_id, tcgplayer_url)""",
        "(unique_id)",
        """UPDATE SET
            (card_unique_id, set_printing_unique_id, card_id, set_id, edition, foiling, rarity, artists,
                art_variations, expansion_slot, flavor_text, flavor_text_plain, image_url, image_rotation_degrees, tcgplayer_product_id, tcgplayer_url) =
            (EXCLUDED.card_unique_id, EXCLUDED.set_printing_unique_id, EXCLUDED.card_id, EXCLUDED.set_id, EXCLUDED.edition, EXCLUDED.foiling, EXCLUDED.rarity, EXCLUDED.artists,
                EXCLUDED.art_variations, EXCLUDED.expansion_slot, EXCLUDED.flavor_text, EXCLUDED.flavor_text_plain, EXCLUDED.image_url, EXCLUDED.image_rotation_degrees, EXCLUDED.tcgplayer_product_id, EXCLUDED.tcgplayer_url)"""
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
                printing['image_url'] = replace_image_url_domain(printing['image_url'], url_for_images)

                card_printing_array.append(printing)

        prep_and_upsert_all(cur, card_printing_array, prep_function, upsert_function)

        print("\nSuccessfully filled card_printings table\n")