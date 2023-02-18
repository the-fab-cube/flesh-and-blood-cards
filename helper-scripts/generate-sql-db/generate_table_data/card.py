import json
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE cards (
            unique_id VARCHAR(21) NOT NULL,
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
            blitz_living_legend BOOLEAN NOT NULL DEFAULT FALSE,
            blitz_living_legend_start TIMESTAMP,
            cc_living_legend BOOLEAN NOT NULL DEFAULT FALSE,
            cc_living_legend_start TIMESTAMP,
            blitz_banned BOOLEAN NOT NULL DEFAULT FALSE,
            blitz_banned_start TIMESTAMP,
            cc_banned BOOLEAN NOT NULL DEFAULT FALSE,
            cc_banned_start TIMESTAMP,
            upf_banned BOOLEAN NOT NULL DEFAULT FALSE,
            upf_banned_start TIMESTAMP,
            commoner_banned BOOLEAN NOT NULL DEFAULT FALSE,
            commoner_banned_start TIMESTAMP,
            blitz_suspended BOOLEAN NOT NULL DEFAULT FALSE,
            blitz_suspended_start TIMESTAMP,
            blitz_suspended_end VARCHAR(1000),
            cc_suspended BOOLEAN NOT NULL DEFAULT FALSE,
            cc_suspended_start TIMESTAMP,
            cc_suspended_end VARCHAR(1000),
            commoner_suspended BOOLEAN NOT NULL DEFAULT FALSE,
            commoner_suspended_start TIMESTAMP,
            commoner_suspended_end VARCHAR(1000),
            PRIMARY KEY (unique_id),
            UNIQUE (name, pitch)
        )
        """

    try:
        print("Creating cards table...")

        # create table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()

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
        exit()

def insert(cur, unique_id, name, pitch, cost, power, defense, health, intelligence, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text,
            played_horizontally, blitz_legal, cc_legal, commoner_legal, blitz_living_legend, blitz_living_legend_start, cc_living_legend, cc_living_legend_start,
            blitz_banned, blitz_banned_start, cc_banned, cc_banned_start, commoner_banned, commoner_banned_start, upf_banned, upf_banned_start,
            blitz_suspended, blitz_suspended_start, blitz_suspended_end, cc_suspended, cc_suspended_start, cc_suspended_end,
            commoner_suspended, commoner_suspended_start, commoner_suspended_end):
    sql = """INSERT INTO cards(unique_id, name, pitch, cost, power, defense, health, intelligence, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text,
            played_horizontally, blitz_legal, cc_legal, commoner_legal, blitz_living_legend, blitz_living_legend_start, cc_living_legend, cc_living_legend_start,
            blitz_banned, blitz_banned_start, cc_banned, cc_banned_start, commoner_banned, commoner_banned_start, upf_banned, upf_banned_start,
            blitz_suspended, blitz_suspended_start, blitz_suspended_end, cc_suspended, cc_suspended_start, cc_suspended_end,
            commoner_suspended, commoner_suspended_start, commoner_suspended_end)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s);"""
    data = (unique_id, name, pitch, cost, power, defense, health, intelligence, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text,
            played_horizontally, blitz_legal, cc_legal, commoner_legal, blitz_living_legend, blitz_living_legend_start, cc_living_legend, cc_living_legend_start,
            blitz_banned, blitz_banned_start, cc_banned, cc_banned_start, commoner_banned, commoner_banned_start, upf_banned, upf_banned_start,
            blitz_suspended, blitz_suspended_start, blitz_suspended_end, cc_suspended, cc_suspended_start, cc_suspended_end,
            commoner_suspended, commoner_suspended_start, commoner_suspended_end)
    try:
        print("Inserting {0} - {1} card with unique id {2}...".format(name, pitch, unique_id))

        # execute the INSERT statement
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        exit()
        raise error

def generate_table_data(cur):
    print("Filling out cards table from card.json...\n")

    path = Path(__file__).parent / "../../../json/english/card.json"
    with path.open(newline='') as jsonfile:
        card_array = json.load(jsonfile)

        for card in card_array:
            unique_id = card['unique_id']
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
            blitz_living_legend_start = card.get('blitz_living_legend_start')
            cc_living_legend = card['cc_living_legend']
            cc_living_legend_start = card.get('cc_living_legend_start')
            blitz_banned = card['blitz_banned']
            blitz_banned_start = card.get('blitz_banned_start')
            cc_banned = card['cc_banned']
            cc_banned_start = card.get('cc_banned_start')
            commoner_banned = card['commoner_banned']
            commoner_banned_start = card.get('commoner_banned_start')
            upf_banned = card['upf_banned']
            upf_banned_start = card.get('upf_banned_start')
            blitz_suspended = card['blitz_suspended']
            blitz_suspended_start = card.get('blitz_suspended_start')
            blitz_suspended_end = card.get('blitz_suspended_end')
            cc_suspended = card['cc_suspended']
            cc_suspended_start = card.get('cc_suspended_start')
            cc_suspended_end = card.get('cc_suspended_end')
            commoner_suspended = card['commoner_suspended']
            commoner_suspended_start = card.get('commoner_suspended_start')
            commoner_suspended_end = card.get('commoner_suspended_end')

            insert(cur, unique_id, name, pitch, cost, power, defense, health, intelligence, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, functional_text_plain, flavor_text, flavor_text_plain, type_text,
            played_horizontally, blitz_legal, cc_legal, commoner_legal, blitz_living_legend, blitz_living_legend_start, cc_living_legend, cc_living_legend_start,
            blitz_banned, blitz_banned_start, cc_banned, cc_banned_start, commoner_banned, commoner_banned_start, upf_banned, upf_banned_start,
            blitz_suspended, blitz_suspended_start, blitz_suspended_end, cc_suspended, cc_suspended_start, cc_suspended_end,
            commoner_suspended, commoner_suspended_start, commoner_suspended_end)

        print("\nSuccessfully filled cards table\n")