import json
import psycopg2
from pathlib import Path

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
            functional_text VARCHAR(10000) NOT NULL,
            functional_text_plain VARCHAR(10000) NOT NULL,
            flavor_text VARCHAR(10000) NOT NULL,
            flavor_text_plain VARCHAR(10000) NOT NULL,
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

def insert(cur, card_unique_id, language, name, pitch, types, card_keywords, abilities_and_effects, ability_and_effect_keywords,
        granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text):
    sql = """INSERT INTO card_translations(card_unique_id, language, name, pitch, types, card_keywords, abilities_and_effects, ability_and_effect_keywords,
                granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s);"""
    data = (card_unique_id, language, name, pitch, types, card_keywords, abilities_and_effects, ability_and_effect_keywords,
        granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text)

    try:
        print("Inserting {0} printing for card {1} ({2} - {3})...".format(
            language,
            card_unique_id,
            name,
            pitch
        ))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()
        raise error

def treat_blank_string_as_boolean(field, value=True):
    if field == '':
        return value

    return field

def treat_blank_string_as_none(field):
    if field == '':
        return 'NULL'

    return "'" + field + "'"

def generate_table_data(cur, language):
    print(f"Filling out cards table from {language} card.json...\n")

    path = Path(__file__).parent / f"../../../json/{language}/card.json"
    with path.open(newline='') as jsonfile:
        card_array = json.load(jsonfile)

        for card in card_array:
            card_unique_id = card['unique_id']
            name = card['name']
            pitch = card['pitch']

            types = card['types']
            card_keywords = card['card_keywords']
            abilities_and_effects = card['abilities_and_effects']
            ability_and_effect_keywords = card['ability_and_effect_keywords']
            granted_keywords = card['granted_keywords']
            functional_text = card['functional_text']
            functional_text_plain = card['functional_text_plain']
            flavor_text = card['flavor_text']
            flavor_text_plain = card['flavor_text_plain']
            type_text = card['type_text']

            insert(cur, card_unique_id, language, name, pitch, types, card_keywords, abilities_and_effects, ability_and_effect_keywords,
                granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text)

        print(f"\nSuccessfully filled cards table with {language} data\n")