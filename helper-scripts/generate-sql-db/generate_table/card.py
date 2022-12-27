import json
import psycopg2
from pathlib import Path
from markdown_patch import unmark

def create_table(cur):
    command = """
        CREATE TABLE cards (
            name VARCHAR(255) NOT NULL,
            pitch VARCHAR(10) COLLATE numeric NOT NULL,
            cost VARCHAR(10) COLLATE numeric NOT NULL,
            power VARCHAR(10) COLLATE numeric NOT NULL,
            defense VARCHAR(10) COLLATE numeric NOT NULL,
            health VARCHAR(10) COLLATE numeric NOT NULL,
            intelligence VARCHAR(10) COLLATE numeric NOT NULL,
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
            played_horizontally BOOLEAN NOT NULL DEFAULT FALSE,
            blitz_legal BOOLEAN NOT NULL DEFAULT TRUE,
            cc_legal BOOLEAN NOT NULL DEFAULT TRUE,
            commoner_legal BOOLEAN NOT NULL DEFAULT TRUE,
            blitz_living_legend TIMESTAMP,
            cc_living_legend TIMESTAMP,
            blitz_banned TIMESTAMP,
            cc_banned TIMESTAMP,
            upf_banned TIMESTAMP,
            commoner_banned TIMESTAMP,
            blitz_suspended_start TIMESTAMP,
            blitz_suspended_end VARCHAR(1000),
            cc_suspended_start TIMESTAMP,
            cc_suspended_end VARCHAR(1000),
            commoner_suspended_start TIMESTAMP,
            commoner_suspended_end VARCHAR(1000),
            PRIMARY KEY(name, pitch)
        )
        """

    try:
        print("Creating cards table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def drop_table(cur):
    command = """
        DROP TABLE IF EXISTS cards;
        """

    try:
        print("Dropping cards table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert(cur, name, pitch, cost, power, defense, health, intelligence, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text,
            played_horizontally, blitz_legal, cc_legal, commoner_legal, blitz_living_legend, cc_living_legend, blitz_banned, cc_banned,
            commoner_banned, upf_banned, blitz_suspended_start, blitz_suspended_end, cc_suspended_start, cc_suspended_end, commoner_suspended_start,
            commoner_suspended_end):
    sql = """INSERT INTO cards(name, pitch, cost, power, defense, health, intelligence, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text,
            played_horizontally, blitz_legal, cc_legal, commoner_legal, blitz_living_legend, cc_living_legend, blitz_banned, cc_banned,
            commoner_banned, upf_banned, blitz_suspended_start, blitz_suspended_end, cc_suspended_start, cc_suspended_end, commoner_suspended_start,
            commoner_suspended_end)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s);"""
    data = (name, pitch, cost, power, defense, health, intelligence, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text,
            played_horizontally, blitz_legal, cc_legal, commoner_legal, blitz_living_legend, cc_living_legend, blitz_banned, cc_banned,
            commoner_banned, upf_banned, blitz_suspended_start, blitz_suspended_end, cc_suspended_start, cc_suspended_end, commoner_suspended_start,
            commoner_suspended_end)
    try:
        print("Inserting {0} - {1} card...".format(name, pitch))

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

def generate_table(cur):
    print("Filling out cards table from card.json...\n")

    path = Path(__file__).parent / "../../../json/card.json"
    with path.open(newline='') as jsonfile:
        card_array = json.load(jsonfile)

        for card in card_array:
            name = card['name']
            pitch = card['pitch']
            cost = card['cost']
            power = card['power']
            defense = card['defense']
            health = card['health']
            intelligence = card['intelligence']
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
            played_horizontally = card['played_horizontally']
            blitz_legal = card['blitz_legal']
            cc_legal = card['cc_legal']
            commoner_legal = card['commoner_legal']
            blitz_living_legend = card['blitz_living_legend']
            cc_living_legend = card['cc_living_legend']
            blitz_banned = card['blitz_banned']
            cc_banned = card['cc_banned']
            commoner_banned = card['commoner_banned']
            upf_banned = card['upf_banned']
            blitz_suspended_start = card['blitz_suspended_start']
            blitz_suspended_end = card['blitz_suspended_end']
            cc_suspended_start = card['cc_suspended_start']
            cc_suspended_end = card['cc_suspended_end']
            commoner_suspended_start = card['commoner_suspended_start']
            commoner_suspended_end = card['commoner_suspended_end']

            insert(cur, name, pitch, cost, power, defense, health, intelligence, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text,
            played_horizontally, blitz_legal, cc_legal, commoner_legal, blitz_living_legend, cc_living_legend, blitz_banned, cc_banned,
            commoner_banned, upf_banned, blitz_suspended_start, blitz_suspended_end, cc_suspended_start, cc_suspended_end, commoner_suspended_start,
            commoner_suspended_end)

        print("\nSuccessfully filled cards table\n")