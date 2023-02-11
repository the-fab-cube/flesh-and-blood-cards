# Download All Images
A Python script that allows users to easily download all known official card images from LSS' website. Alternatively, can download all cards from just one set at a time.

## Running the Script with System Python

### Initial Setup
1. Ensure your system python is the same version as or compatible with the python version listed in `.python-version`
2. Ensure all required packages are installed.

### Running the Script
1. Run `python main.py` to download all images.
2. Run with the flag `-s [SETID]` to download only images from that set.
    * Ex: `python main.py -s WTR`

## Running the Script with Pyenv

### Initial Setup
1. Install [pyenv](https://github.com/pyenv/pyenv).
2. Run `pyenv install` to install Python version.
3. Install [poetry](https://python-poetry.org/).
    * I recommend using `pyenv exec pip install poetry`.
4. Run `pyenv exec poetry install` to install packages.

### Running the Script
1. Run `pyenv exec poetry run python main.py` to download all images.
2. Run with the flag `-s [SETID]` to download only images from that set.
    * Ex: `pyenv exec poetry run python main.py -s WTR`