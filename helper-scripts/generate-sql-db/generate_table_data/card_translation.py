import json
import psycopg2
from pathlib import Path

from helpers import upsert_array, prep_and_upsert_all

def create_table(cur):
    command = """
        CREATE TABLE card_translations (
            card_unique_id VARCHAR(21) NOT NULL,
            language VARCHAR(10) NOT NULL,
            name VARCHAR(255) NOT NULL,
            pitch VARCHAR(10) COLLATE numeric NOT NULL,
            types VARCHAR(255)[] NOT NULL,
            card_keywords VARCHAR(255)[] NOT NULL,
            abilities_and_effects VARCHAR(255)[] NOT NULL,
            ability_and_effect_keywords VARCHAR(255)[] NOT NULL,
            granted_keywords VARCHAR(255)[] NOT NULL,
            removed_keywords VARCHAR(255)[] NOT NULL,
            interacts_with_keywords VARCHAR(255)[] NOT NULL,
            functional_text VARCHAR(10000) NOT NULL,
            functional_text_plain VARCHAR(10000) NOT NULL,
            type_text VARCHAR(1000) NOT NULL,
            FOREIGN KEY (card_unique_id) REFERENCES cards (unique_id),
            PRIMARY KEY (card_unique_id, language)
        )
        """

    try:
        print("Creating card_translations table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS card_translations
        """

    try:
        print("Dropping card_translations table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

def prep_function(card, language):
    card_unique_id = card['unique_id']
    name = card['name']
    pitch = card['pitch']

    types = card['types']
    card_keywords = card['card_keywords']
    abilities_and_effects = card['abilities_and_effects']
    ability_and_effect_keywords = card['ability_and_effect_keywords']
    granted_keywords = card['granted_keywords']
    removed_keywords = card['removed_keywords']
    interacts_with_keywords = card['interacts_with_keywords']
    functional_text = card['functional_text']
    functional_text_plain = card['functional_text_plain']
    type_text = card['type_text']

    print("Prepping {0} printing for card {1} ({2} - {3})...".format(
        language,
        card_unique_id,
        name,
        pitch
    ))

    return (card_unique_id, language, name, pitch, types, card_keywords, abilities_and_effects, ability_and_effect_keywords,
        granted_keywords, removed_keywords, interacts_with_keywords, functional_text, functional_text_plain, type_text)

def upsert_function(cur, card_translations):
    print("Upserting {} card_translations".format(len(card_translations)))

    upsert_array(
        cur,
        "card_translations",
        card_translations,
        14,
        """(card_unique_id, language, name, pitch, types, card_keywords, abilities_and_effects, ability_and_effect_keywords,
            granted_keywords, removed_keywords, interacts_with_keywords, functional_text, functional_text_plain, type_text)""",
        "(card_unique_id, language)",
        """UPDATE SET
        (name, pitch, types, card_keywords, abilities_and_effects, ability_and_effect_keywords,
            granted_keywords, removed_keywords, interacts_with_keywords, functional_text, functional_text_plain, type_text) =
        (EXCLUDED.name, EXCLUDED.pitch, EXCLUDED.types, EXCLUDED.card_keywords, EXCLUDED.abilities_and_effects, EXCLUDED.ability_and_effect_keywords,
            EXCLUDED.granted_keywords, EXCLUDED.removed_keywords, EXCLUDED.interacts_with_keywords, EXCLUDED.functional_text, EXCLUDED.functional_text_plain, EXCLUDED.type_text)
        """
    )

def generate_table_data(cur, language):
    print(f"Filling out card_translations table from {language} card.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/card.json"
    with path.open(newline='') as jsonfile:
        card_array = json.load(jsonfile)

        prep_and_upsert_all(cur, card_array, prep_function, upsert_function, language)

        print(f"\nSuccessfully filled cards table with {language} data\n")