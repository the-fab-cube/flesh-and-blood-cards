import csv
import psycopg2
from pathlib import Path

def create_table(cur):
    command = """
        CREATE TABLE cards (
            ids VARCHAR(15)[] NOT NULL,
            set_ids VARCHAR(15)[] NOT NULL,
            name VARCHAR(255) NOT NULL,
            pitch VARCHAR(10),
            cost VARCHAR(10),
            power VARCHAR(10),
            defense VARCHAR(10),
            health VARCHAR(10),
            intelligence VARCHAR(10),
            rarities VARCHAR(255)[] NOT NULL,
            types VARCHAR(255)[] NOT NULL,
            card_keywords VARCHAR(255)[],
            abilities_and_effects VARCHAR(255)[],
            ability_and_effect_keywords VARCHAR(255)[],
            granted_keywords VARCHAR(255)[],
            functional_text VARCHAR(10000),
            flavor_text VARCHAR(10000),
            type_text VARCHAR(1000),
            played_horizontally BOOLEAN NOT NULL DEFAULT FALSE,
            blitz_restricted BOOLEAN NOT NULL DEFAULT FALSE,
            blitz_legal BOOLEAN NOT NULL DEFAULT TRUE,
            cc_legal BOOLEAN NOT NULL DEFAULT TRUE,
            variations VARCHAR(255)[] NOT NULL,
            image_urls VARCHAR(1000)[] NOT NULL
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
        DROP TABLE IF EXISTS cards
        """

    try:
        print("Dropping cards table...")

        # drop table
        cur.execute(command)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert(cur, ids, set_ids, name, pitch, cost, power, defense, health, intelligence, rarities, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, flavor_text, type_text, played_horizontally, blitz_restricted,
            blitz_legal, cc_legal, variations, image_urls):
    sql = """INSERT INTO cards(ids, set_ids, name, pitch, cost, power, defense, health, intelligence, rarities, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, flavor_text, type_text, played_horizontally, blitz_restricted,
            blitz_legal, cc_legal, variations, image_urls)
            VALUES('{{{0}}}', '{{{1}}}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{{{9}}}', '{{{10}}}', '{{{11}}}', '{{{12}}}',
            '{{{13}}}', '{{{14}}}', '{15}', '{16}', '{17}', '{18}', '{19}',
            '{20}', '{21}', '{{{22}}}', '{{{23}}}');"""
    try:
        print("Inserting {0} - {1} card...".format(name, pitch))

        # execute the INSERT statement
        cur.execute(sql.format(ids, set_ids, name, pitch, cost, power, defense, health, intelligence, rarities, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, flavor_text, type_text, played_horizontally, blitz_restricted,
            blitz_legal, cc_legal, variations, image_urls))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error

def generate_table(cur):
    print("Filling out cards table from card.csv...\n")

    path = Path(__file__).parent / "../../csvs/card.csv"
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            ids = row[0]
            set_ids = row[1]
            name = row[2]
            pitch = row[3]
            cost = row[4]
            power = row[5]
            defense = row[6]
            health = row[7]
            intelligence = row[8]
            rarities = row[9]
            types = row[10]
            card_keywords = row[11]
            abilities_and_effects = row[12]
            ability_and_effect_keywords = row[13]
            granted_keywords = row[14]
            functional_text = row[15]
            flavor_text = row[16]
            type_text = row[17]
            played_horizontally = row[18]
            blitz_restricted = row[19]
            blitz_legal = row[20]
            cc_legal = row[21]
            variations = row[22]
            image_urls = row[23]

            if played_horizontally == '':
                played_horizontally = False
            if blitz_restricted == '':
                blitz_restricted = False
            if blitz_legal == '':
                blitz_legal = True
            if cc_legal == '':
                cc_legal = True

            functional_text = functional_text.replace("'", "''")

            insert(cur, ids, set_ids, name, pitch, cost, power, defense, health, intelligence, rarities, types, card_keywords, abilities_and_effects,
            ability_and_effect_keywords, granted_keywords, functional_text, flavor_text, type_text, played_horizontally, blitz_restricted,
            blitz_legal, cc_legal, variations, image_urls)

            # print(', '.join(row))

        print("\nSuccessfully filled cards table\n")