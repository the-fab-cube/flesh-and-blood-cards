# Generate SQL DB
A Python script that generates SQL tables from the JSON files within the given PostgreSQL database, replacing the LSS image base URL with the given image base URL (since it's polite to not use LSS hosted data for your own applications).

NOTE: This will delete and regenerate the tables every run. The tables are not intended to be edited outside of running this script. Also ensure that anything using foreign keys to associate to these tables do not cascade on delete, or regenerating this script will wipe data from your database!

## Running the Script with System Python

### Initial Setup
1. Ensure your system python is the same version as or compatible with the python version listed in `.python-version`
2. Ensure all required packages are installed.

### Running the Script
1. Run `python main.py -d <database-name> -u <user> -p <password> -H <host> -P <port> -i <images-base-url>` to run the SQL database generator.
2. Add `-r` as an option to delete all the tables and regenerate them from scratch.

## Running the Script with Pyenv

### Initial Setup
1. Install [pyenv](https://github.com/pyenv/pyenv).
2. Run `pyenv install` to install Python version.
3. Install [poetry](https://python-poetry.org/).
    * I recommend using `pyenv exec pip install poetry`.
4. Run `pyenv exec poetry install` to install packages.

### Running the Script
1. Run `pyenv exec poetry run python main.py -d <database-name> -u <user> -p <password> -H <host> -P <port> -i <images-base-url>` to run the SQL database generator.
2. Add `-r` as an option to delete all the tables and regenerate them from scratch.