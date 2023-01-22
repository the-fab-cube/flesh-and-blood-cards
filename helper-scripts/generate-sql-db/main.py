import getopt
import psycopg2
import sys
from tables import *

url_for_images = None
database_name = None
user = None
password = None
host = None
port = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:d:u:p:H:P:")
except getopt.GetoptError:
    print('main.py -d <database-name> -u <user> -p <password> -H <host> -P <port> -i <images-base-url>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('main.py -d <database-name> -u <user> -p <password> -H <host> -P <port> -i <images-base-url>')
        sys.exit()
    elif opt in ("-i", "--images-base-url"):
        url_for_images = arg
        print("Using", url_for_images, "for images")
    elif opt in ("-d", "--database-name"):
        database_name = arg
    elif opt in ("-u", "--user"):
        user = arg
    elif opt in ("-p", "--password"):
        password = arg
    elif opt in ("-H", "--host"):
        host = arg
    elif opt in ("-P", "--port"):
        port = arg

if database_name is None:
    print("ERROR: Please provide a database name (-d, --database-name)")
    sys.exit()
if user is None:
    print("ERROR: Please provide a user (-u, --user)")
    sys.exit()
if password is None:
    print("ERROR: Please provide a password (-p, --password)")
    sys.exit()
if host is None:
    print("ERROR: Please provide a host (-H, --host)")
    sys.exit()
if port is None:
    print("ERROR: Please provide a port (-P, --port)")
    sys.exit()

print("Using", database_name, "for database name\n")

#establishing the connection to postgres
conn = None
try:
    conn = psycopg2.connect(
        database=database_name, user=user, password=password, host=host, port=port
    )
    conn.autocommit = False

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    ## Get current database names
    cursor.execute("SELECT datname FROM pg_database;")

    list_database = cursor.fetchall()

    ## Create database if it doesn't exist already
    if (database_name,) not in list_database:
        print("'{}' database does not exist, creating it.".format(database_name))
        cursor.execute('''CREATE database fabcards''')
        print("'{}' database created successfully...........".format(database_name))

    ## Add collations
    cursor.execute("CREATE COLLATION IF NOT EXISTS numeric (provider = icu, locale = 'en@colNumeric=yes');")

    ## Drop existing tables, recreate them, and then fill them with data
    drop_tables(conn)
    print()
    create_tables(conn)
    print()
    generate_all_table_data(conn, url_for_images)

    conn.commit()
except psycopg2.DatabaseError as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

print('Done creating tables from CSVs!')