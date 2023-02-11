#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

cd ./generate-csv-htmls
./generate.sh || exit $?
cd ..

echo ""

cd ./generate-json-schema-htmls
./generate.sh || exit $?
cd ..
