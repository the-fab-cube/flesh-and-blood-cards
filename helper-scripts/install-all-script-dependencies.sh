#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

# Clean CSVs
echo "Installing clean-csvs script dependencies..."

cd ./clean-csvs

if type pyenv >/dev/null 2>&1; then
    pyenv exec poetry install
fi

cd ..

# Download All Images
echo "Installing download-all-images script dependencies..."

cd ./download-all-images

if type pyenv >/dev/null 2>&1; then
    pyenv exec poetry install
fi

cd ..

# Generate Artists
echo "Installing generate-artists script dependencies..."

cd ./generate-artists

if type pyenv >/dev/null 2>&1; then
    pyenv exec poetry install
fi

cd ..

# Generate CSV HTMLs
echo "Installing generate-csv-htmls script dependencies..."

cd ./generate-csv-htmls

if type pyenv >/dev/null 2>&1; then
    pyenv exec poetry install
fi

cd ..

# Generate JSON
echo "Installing generate-json script dependencies..."

cd ./generate-json

if type pyenv >/dev/null 2>&1; then
    pyenv exec poetry install
fi

cd ..

# Generate JSON Schema HTMLs
echo "Installing generate-json-schema-htmls script dependencies..."

cd ./generate-json-schema-htmls

if type pyenv >/dev/null 2>&1; then
    pyenv exec poetry install
fi

cd ..

# Generate SQL DB
echo "Installing generate-sql-db script dependencies..."

cd ./generate-sql-db

if type pyenv >/dev/null 2>&1; then
    pyenv exec poetry install
fi

cd ..

# Generate Unique IDs
echo "Installing generate-unique-ids script dependencies..."

cd ./generate-unique-ids

source ~/.nvm/nvm.sh
if command -v nvm &> /dev/null
then
    nvm use
fi
npm install

cd ..

# JSON Validation
echo "Installing json-validation script dependencies..."

cd ./json-validation

source ~/.nvm/nvm.sh
if command -v nvm &> /dev/null
then
    nvm use
fi
npm install

cd ..

# Validate References
echo "Installing validate-references script dependencies..."

cd ./validate-references

if type pyenv >/dev/null 2>&1; then
    pyenv exec poetry install
fi

cd ..