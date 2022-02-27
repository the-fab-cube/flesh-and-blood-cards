import csv
import psycopg2

def insert_edition(conn, id, name):
    sql = """INSERT INTO editions(id, name)
             VALUES(%s, %s) RETURNING id;"""
    try:
        print("Inserting {} edition...".format(id))

        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (id,name))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def generate_edition_table(conn):
    print("Filling out editions table from edition.csv...\n")

    with open('../csvs/edition.csv', newline='') as csvfile:
        edition_reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(edition_reader)

        for row in edition_reader:
            id = row[0]
            name = row[1]
            insert_edition(conn, id, name)
            print(', '.join(row))

        print("\nSuccessfully filled editions table\n")