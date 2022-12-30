#!/bin/bash

cd ./generate-csv-htmls
./generate.sh
cd ..

echo ""

cd ./generate-json-schema-htmls
./generate.sh
cd ..