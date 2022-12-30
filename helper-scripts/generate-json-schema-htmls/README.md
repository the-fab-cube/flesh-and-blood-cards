# Generate JSON Schema HTMLs
A Python script that generates HTML files from the JSON Schema files.

## Initial Setup
1. Install [pyenv](https://github.com/pyenv/pyenv).
2. Run `pyenv install` to install Python version.
3. Install [poetry](https://python-poetry.org/).
    * I recommend using `pyenv exec pip install poetry`.
4. Run `pyenv exec poetry install` to install packages.

## Running the Script
1. Run `pyenv exec poetry run generate-schema-doc --config-file conf.yaml [json-schema-input-filepath] [html-output-filepath]` to generate the JSON Schema HTML displays for the input filepath.

    OR

2. Run `./generate.sh` as a shortcut for the above command.