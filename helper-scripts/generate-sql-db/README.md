### Initial Setup
1. Install pyenv
2. Run `pyenv install` to install Python version
2. Install (poetry)[https://python-poetry.org/]
    a. I recommend using `pyenv exec pip install poetry`
3. Run `pyenv exec poetry install` to install packages
4. Run `pyenv exec poetry run python main.py -d <database-name> -u <user> -p <password> -H <host> -P <port> -i <images-base-url>` to run the SQL database generator