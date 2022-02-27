def create_tables(conn = None):
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE editions (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """,
    )

    try:
        print("Creating tables to import CSV data into...\n")

        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def drop_tables(conn = None):
    commands = (
        """
        DROP TABLE IF EXISTS editions
        """,
    )

    try:
        print("Dropping existing tables that were created from CSVs...\n")

        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)