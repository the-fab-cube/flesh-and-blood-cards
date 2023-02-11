# Generate JSON Schema HTMLs
A Python script that generates HTML files from the JSON Schema files.

## Running the Script with System Python

### Initial Setup
1. Ensure your system python is the same version as or compatible with the python version listed in `.python-version`
2. Ensure all required packages are installed.

### Running the Script
1. Run `generate-schema-doc --config-file conf.yaml [json-schema-input-filepath] [html-output-filepath]` to generate the JSON Schema HTML displays for the input filepath.

    OR

2. Run `./generate.sh` as a shortcut for the above command.

## Running the Script with Pyenv

### Initial Setup
1. Install [pyenv](https://github.com/pyenv/pyenv).
2. Run `pyenv install` to install Python version.
3. Install [poetry](https://python-poetry.org/).
    * I recommend using `pyenv exec pip install poetry`.
4. Run `pyenv exec poetry install` to install packages.

### Running the Script
1. Run `pyenv exec poetry run generate-schema-doc --config-file conf.yaml [json-schema-input-filepath] [html-output-filepath]` to generate the JSON Schema HTML displays for the input filepath.

    OR

2. Run `./generate.sh` as a shortcut for the above command.