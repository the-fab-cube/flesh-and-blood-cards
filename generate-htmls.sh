#!/bin/bash

pyenv exec csvtotable csvs/artist.csv web/csvs/artist.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/card.csv web/csvs/card.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/edition.csv web/csvs/edition.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/foiling.csv web/csvs/foiling.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/icon.csv web/csvs/icon.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/keyword.csv web/csvs/keyword.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/rarity.csv web/csvs/rarity.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/set.csv web/csvs/set.html -d $'\t' -q $'"' -o
pyenv exec csvtotable csvs/type.csv web/csvs/type.html -d $'\t' -q $'"' -o

echo ""

cd ./generate-json-markdown
./generate.sh
cd ..