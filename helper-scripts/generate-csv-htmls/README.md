# Generate CSV HTMLs
A Python script that generates the HTML files for viewing the CSVs on the web.

## Running the Script with System Python

### Initial Setup
1. Ensure your system python is the same version as or compatible with the python version listed in `.python-version`
2. Ensure all required packages are installed.

### Running the Script
1. Run `csvtotable [csv-input-filepath] [html-output-filepath] -d $'\t' -q $'"' -o` to generate an HTML file for the CSV.

    OR

2. Run `./generate.sh` to generate HTMLs for all the current CSV files.

## Running the Script with Pyenv

### Initial Setup
1. Install [pyenv](https://github.com/pyenv/pyenv).
2. Run `pyenv install` to install Python version.
3. Install [poetry](https://python-poetry.org/).
    * I recommend using `pyenv exec pip install poetry`.
4. Run `pyenv exec poetry install` to install packages.

### Running the Script
1. Run `pyenv exec poetry run csvtotable [csv-input-filepath] [html-output-filepath] -d $'\t' -q $'"' -o` to generate an HTML file for the CSV.

    OR

2. Run `./generate.sh` to generate HTMLs for all the current CSV files.